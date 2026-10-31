"""F2 round-1 build: cards, candidate rows (1.5x), the G6 QC sample, the S5 mix-tuning dev items and the depth sweep.

Run:  .venv/bin/python -m gen.build [--part cand|qc|dev|all] [--only S1,S2] [--limit N]
Writes out/candidates_r1.jsonl (+ relations), out/qc_sample.jsonl (+ relations), out/mixdev_S5.jsonl, card and
side files; every row passes fmt1 loader_check and the G3 round trip here (rows that fail are never written; failures
are counted and must be 0 for the gate).
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections import Counter, defaultdict

from . import attack as ATK, canon, options as O, packs, rowkit
from .common import LEAN, OUT, TMP, progress, rng_for, uhash, write_jsonl, write_json
from .parse import parse_row
from .money import Reject
from .mgen import predraw

ENGINES = {}


def engine(name):
    if not ENGINES:
        from . import eng_money
        ENGINES["money"] = eng_money
        try:
            from . import eng_band
            ENGINES["band"] = eng_band
        except ImportError:
            pass
        try:
            from . import eng_date
            ENGINES["date"] = eng_date
        except ImportError:
            pass
        try:
            from . import eng_stmt
            ENGINES["stmt"] = eng_stmt
        except ImportError:
            pass
    return ENGINES[name]


SAMPLER_ENGINE = {"S1": "money", "S2": "money", "S3": "band", "S4": "date", "S5": "stmt"}
BUDGET = {"S1": 1200, "S2": 1275, "S3": 1125, "S4": 1125}     # 1.5 x the r1 rows of G0 1.2
PLAN = {
    "S1": [("YN-T", "closed", 9), ("CH-V", "closed", 3), ("CH-V", "open", 2), ("CH-O", "closed", 2), ("CH-O", "open", 1),
           ("CL", "closed", 4)],
    "S2": [("YN-T", "closed", 15), ("CH-V", "closed", 4), ("CH-O", "closed", 2)],
    "S3": [("CH-B", "closed", 4), ("CH-V", "closed", 2), ("CH-V", "open", 2), ("YN-T", "closed", 7), ("CL", "closed", 4)],
    "S4": [("YN-D", "closed", 9), ("CH-D", "closed", 2), ("CH-D", "open", 2), ("CH-C", "closed", 1),
           ("CH-O", "closed", 1), ("CH-O", "open", 1), ("CL", "closed", 3)],
}
# v1.1: two more S1 cards are open-world, so round 1 has 10 open-world cards (G0 1: "r1 10-12"); v1.0 planned 8
OPEN_EXTRA = {("S1", "CH-V", 2), ("S1", "CH-O", 1)}
# v1.1: per-card generator options. The S4 open-world date-window card drew a business-day deadline whose card text
# (printed twice by the layout) left ~99% of its rows at >= 1,900 tokens; it uses a calendar-day deadline instead
CARD_OPTS = {("S4", "CH-O", 1): {"rule_kind": "cal", "try_mult": 20}}
# repair r1.1: case lists need >= 2 interacting per-case fields, or the one qualifying case is always the extreme of
# its visible primary column (v1.0: 77% of case-list rows). S4 case lists carry a per-case extension condition, S3
# case lists a computed banding amount (quantity x price per case)
for _j in range(3):
    CARD_OPTS[("S4", "CL", _j)] = {"force_ext": True}
for _j in range(4):
    CARD_OPTS[("S3", "CL", _j)] = {"computed": True}
FEWSHOT = {("S1", "YN-T", 0), ("S1", "CH-V", 0), ("S2", "YN-T", 1), ("S3", "YN-T", 0), ("S4", "YN-D", 0),
           ("S3", "CH-B", 0)}


def plan_cards(only=None):
    """The 80 round-1 training cards, one per training pack (SC4b)."""
    tr, he = packs.split()
    cards = []
    pi = 0
    short_n = 0
    for s in ("S1", "S2", "S3", "S4"):
        idx = Counter()
        for sch, world0, n in PLAN[s]:
            for i in range(n):
                j = idx[sch]
                idx[sch] += 1
                world = "open" if (s, sch, j) in OPEN_EXTRA else world0
                instr = "fewshot" if (s, sch, j) in FEWSHOT else ("inverted" if sch == "CL" else "std")
                pack = tr[pi]
                pi += 1
                cid = f"F2.{s}.{pack['id']}.{sch}.{instr}"
                c = {"card_id": cid, "sampler": s, "schema": sch, "world": world, "instr": instr, "pack_obj": pack,
                     "held_out": False}
                if instr == "std" and sch != "CL" and world == "closed" and s in ("S1", "S2") and uhash("F2-short", cid) < 0.4:
                    c["short"] = True
                c.update(CARD_OPTS.get((s, sch, j), {}))
                cards.append(c)
    if only:
        cards = [c for c in cards if c["sampler"] in only]
    return cards


def is_named_card(c):
    return (c["schema"] == "CH-O" and c["sampler"] in ("S1", "S2")) or (c["sampler"] == "S3" and c["schema"] in ("CH-B", "CH-V"))


def card_weight(c):
    """Row weight of a card inside its sampler budget. Repair r2: named-option cards weigh 1.25 (v1.2: named-option
    rows 24.0% of choice rows vs about 30 (25-35), section 6; masked 11.3 and swapped 4.2 scale to about 13.5 and 5)."""
    if c["schema"] == "CL":
        return 2.2
    return 1.2 if is_named_card(c) else 1.0


def card_targets(cards):
    """Candidate rows per card (all twins included), summing to each sampler's budget."""
    out = {}
    by = defaultdict(list)
    for c in cards:
        by[c["sampler"]].append(c)
    for s, cs in by.items():
        w = {c["card_id"]: card_weight(c) for c in cs}
        tot = sum(w.values())
        bud = BUDGET[s]
        acc = 0
        for i, c in enumerate(cs):
            n = int(round(bud * w[c["card_id"]] / tot))
            if i == len(cs) - 1:
                n = bud - acc
            out[c["card_id"]] = n
            acc += n
    return out


class Out:
    def __init__(self):
        self.rows, self.rels, self.side = [], [], []
        self.fail = Counter()
        self.hashes = set()
        self.last_fail = None


_TOK = {}


def real_tokens(row):
    """Real-tokenizer length of the trained and served prompt (cygnet, schema_branch_mark; `instructions` and the option
    texts appear twice in it), chat template applied (3.7, G15)."""
    if not _TOK:
        import hashlib as _h
        import random as _r
        sys.path.insert(0, str(LEAN))
        import decoder_io as dio
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        from transformers import AutoTokenizer
        _TOK["tok"] = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
        _TOK["dio"] = dio
    tok, dio = _TOK["tok"], _TOK["dio"]
    n = len(row["options"]) if row["qtype"] == "choice" else 2
    if n > len(dio.WIDE):     # placeholder two-letter labels past Z, as fmt1's loader check (a Readout fills real ones)
        import string as _s
        U = _s.ascii_uppercase
        dio.WIDE = list(U) + [a + b for a in U for b in U]
    prompt = dio.user_msg(row, list(range(n)))
    return len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, prompt), add_special_tokens=False)["input_ids"])


def emit(out, row, P, res, parse_check=True):
    if not res["ok"]:
        out.fail["loader:" + res["problems"][0][:50]] += 1
        return False
    if parse_check:
        g = rowkit.g3_check(row, P, parse_row)
        if not g["ok"]:
            out.fail["g3:" + g["problems"][0][:60]] += 1
            return False
    t = real_tokens(row)
    if t >= 1900:
        out.fail["tokens_ge_1900"] += 1
        out.last_fail = "tokens"
        return False
    row["meta"]["tokens"] = t
    out.rows.append(row)
    return True


VALUE_SCHEMAS = ("CH-V", "CH-D", "CH-C")
PREDRAW_KEYS = ("k", "needed", "ncases", "u_none", "gold_none", "show_none", "k_pref", "u_rank", "u_crank", "aff", "u_k", "u_side", "u_grp")


class AdjBal:
    """Repair r2: emitted-row counts of has:x and dec:x (label schemas) / bind:x (value schemas) per adjustment over
    the part being built. Each new base row focuses the adjustment furthest from 50% among its own has:x tags and
    wants the status that corrects it (v1.2 focused one random x per row with a fair coin, so the other has:x tags of
    multi-adjustment rows stayed at their natural rates: dec 0-44%, bind 7-85% vs 50 +/- 5, section 6; A44, R2-18)."""

    def __init__(self):
        self.n, self.d, self.seen = Counter(), Counter(), 0
        self.rows_n, self.sem_n = 0, 0
        O.ABST_DEF.clear()                       # one abstain-deficit ledger per part

    def sem_short(self):
        """Repair r2: emitted rows with >= 1 sem:* below SEM_TARGET (v1.2: 31.4% vs >= 40, section 6)."""
        return self.rows_n == 0 or self.sem_n / self.rows_n < SEM_TARGET

    def update(self, rows):
        for r in rows[self.seen:]:
            O.abst_note(r)
            self.rows_n += 1
            self.sem_n += int(any(t.startswith("sem:") for t in r["meta"]["edge"]))
            kind = "bind" if r["meta"]["card_id"].split(".")[3] in VALUE_SCHEMAS else "dec"
            tg = set(r["meta"]["edge"])
            for t in tg:
                if t.startswith("has:"):
                    self.n[(kind, t[4:])] += 1
                    self.d[(kind, t[4:])] += int(f"{kind}:{t[4:]}" in tg)
        self.seen = len(rows)

    def deficit(self, kind, x):
        return 0.5 * self.n[(kind, x)] - self.d[(kind, x)]


SEM_TARGET = 0.46


def cand_sem(eng, card, cand, var):
    """True / False: the candidate has a decisive semantic dimension (sem:*), computed as to_row will; None when the
    engine cannot tell before rendering (dates) or the card has shown none in its first 24 checks."""
    st = card.setdefault("_sem_probe", [0, 0])
    if st[0] >= 24 and st[1] == 0:
        return None
    try:
        if card.get("engine") == "money":
            ok = bool(eng.AM.decisive_dims(card, cand, var))
        elif card.get("engine") == "band":
            ok = bool(eng.decisive_dims(card, cand))
        else:
            return None
    except Exception:
        return None
    st[0] += 1
    st[1] += int(ok)
    return ok


def focus_ok_bal(card, spec, bal, rng):
    tags = set(spec.get("tags", []))
    has = sorted(t[4:] for t in tags if t.startswith("has:"))
    if spec.get("qkind") == "thr" and spec.get("placement") and not spec["placement"].get("near"):
        has = [x for x in has if x != "round"]
    if not has:
        return True
    kind = "bind" if card["schema"] in VALUE_SCHEMAS else "dec"
    ds = [(abs(bal.deficit(kind, x)), rng.random(), x) for x in has]
    dmax, _, x = max(ds)
    if dmax < 1.0:
        return (f"{kind}:{x}" in tags) == (rng.random() < 0.5)
    return (f"{kind}:{x}" in tags) == (bal.deficit(kind, x) > 0)


def focus_ok(card, spec, want_flag, rng):
    """Adjustment balance (A44, R2-18): one adjustment x of the row, picked at random among its has:x tags, binds
    (value schemas) or is decisive (label schemas) as drawn (50%). Far yes/no rows are exempt for rounding (A43)."""
    tags = set(spec.get("tags", []))
    has = sorted(t[4:] for t in tags if t.startswith("has:"))
    if spec.get("qkind") == "thr" and spec.get("placement") and not spec["placement"].get("near"):
        has = [x for x in has if x != "round"]
    if not has:
        return True
    x = has[int(rng.random() * len(has))]
    kind = "bind" if card["schema"] in VALUE_SCHEMAS else "dec"
    return (f"{kind}:{x}" in tags) == want_flag


def build_card_rows(card, eng, target, rng, out, used_ids, purpose, global_hashes, nb_start=0, id_tag=None,
                    deadline=None):
    """Bases with their twins until the card holds `target` rows (or until `deadline`, a time.time() value)."""
    n0 = len(out.rows)
    used_e = set()
    nb = nb_start
    tries = 0
    var_n = len(card.get("variants", []))
    yn = card["qtype"] == "noul"
    dead = 0
    redraws = 0
    held = None          # predrawn statuses (k, NEI needed, case count, abstain uniform) kept until a base row is out
    while len(out.rows) - n0 < target and tries < target * card.get("try_mult", 6):
        if deadline is not None and time.time() > deadline:
            out.fail[f"card_time_budget:{card['card_id']}"] += 1
            break
        tries += 1
        r = rng.random()
        var = 0
        if var_n and r < 0.4:
            var = 1 + int(rng.random() * var_n)
        # repair r1.1: the card variant is held with the other predrawn statuses, so a retry never moves an
        # NEI-needed / abstain-gold draw onto another variant (v1.0: abstain gold over-represented on var >= 1 rows)
        if held is not None and "_var" in held:
            var = held["_var"]
        want = {}
        unit = None
        neg_single = 0
        if yn:
            u = rng.random()
            if u < 0.13 and var == 0:
                unit = "neg"
            elif u < 0.20:
                neg_single = 1
            elif u < 0.27:
                unit = "attack"
            elif u < 0.31:
                unit = "inert"
        else:
            u = rng.random()
            if u < 0.06:
                unit = "attack"
            elif u < 0.10:
                unit = "inert"
        if held is not None and "_unit" in held:
            unit, neg_single = held["_unit"], held["_neg"]     # repair r1.1: held with the label draw
        want["neg"] = neg_single
        # XF01 / SC2: abstain and NEI statuses are drawn once and held across every retry (Reject, the adjustment
        # balance pick, a hash clash, a token or render failure) until a base row is written, so retries never bias
        # them (v1.1; v1.0 re-drew them on each retry)
        if held is not None and not (card["schema"] == "CL" and held.get("ncases") not in card.get("ncase_choices", [])):
            want.update(held)
        want = predraw(card, rng, want)
        held = {k: want[k] for k in PREDRAW_KEYS if k in want}
        held["_var"] = var
        held["_unit"] = unit
        held["_neg"] = neg_single
        spec = None
        want_flag = rng.random() < 0.5
        if not hasattr(out, "adjbal"):
            out.adjbal = AdjBal()
        out.adjbal.update(out.rows)
        sem_want = out.adjbal.sem_short()
        for ft in range(16):                     # repair r2: 16 focus tries (was 8)
            try:
                cand = eng.gen_row(card, rng, var, want)
            except Reject:
                continue
            spec = cand
            if focus_ok_bal(card, cand, out.adjbal, rng) and not (
                    sem_want and cand_sem(eng, card, cand, var) is False):     # repair r2 (was focus_ok, fair coin)
                break
        if spec is None:
            dead += 1
            if dead == 4:
                # a held draw that this card cannot build: redraw it (counted). Repair r2: for the first 10 redraws of
                # a card the label-side draws (aff, NEI needed, abstain gold, unit / negation) are kept and only the
                # structure draws are redrawn, so a structure that is harder to build for one label never shifts the
                # label rates (smoke r2: NEI gold 39.0% vs 33.3 at k 3 when open inert rows needed ordered options)
                keep = {k: held[k] for k in ("aff", "needed", "gold_none", "u_none", "_unit", "_neg")
                        if held is not None and k in held} if redraws < 10 else {}
                held = keep or None
                out.fail[f"held_redraw:{card['card_id']}"] += 1
                redraws += 1
                dead = 0 if redraws < 25 else 8
            if dead >= 8:
                out.fail[f"card_stalled:{card['card_id']}"] += 1
                break
            continue
        dead = 0
        if spec.get("_needs_depth"):
            spec["depth"] = spec.get("depth", 1)
        h = canon.structure_hash(canon.canonize(spec["LP"]))
        if h in global_hashes:
            continue
        global_hashes.add(h)
        nb += 1
        bid = f"{id_tag or card['short_id']}.{nb:04d}"
        eid = eng.new_eid(card, rng, used_e)
        if yn:
            spec["tf"] = (neg_single > 0) or (rng.random() < 0.5)
        noop = None
        if rng.random() < 0.35 and spec.get("qkind") != "cases":
            noop = eng.inert_pair(card, spec, rng, eng.labels_in(card))
        try:
            row, res, P, q = eng.to_row(card, spec, rng, row_id=bid, var=var, eid=eid, inert=noop)
        except Exception as e:
            out.fail["render:" + type(e).__name__ + ":" + str(e)[:40]] += 1
            continue
        row["group_id"] = bid
        row["call_id"] = bid
        if noop:
            row["meta"]["edge"] = sorted(set(row["meta"]["edge"] + ["noop:1"]))
        out.last_fail = None
        if spec.get("cases"):
            card.setdefault("_tok_try", Counter())[len(spec["cases"])] += 1     # repair r2: token-drop denominator
        if not emit(out, row, P, res):
            if out.last_fail == "tokens" and spec.get("cases"):
                # case lists too long for the token cap on this card: drop case counts at or above this one
                ncs = len(spec["cases"])
                # repair r1.1: a count is dropped only after 3 token failures at or above it (v1.0 dropped every
                # larger count on the first failure, leaving most S3 / S4 case lists at 5 cases)
                # repair r2: a count (and every larger one) is dropped only when, over rendered rows with at least that
                # many cases, >= 4 failed the token cap and they are >= 50% of those rows (v1.2 dropped after 3 token
                # failures at any count <= it, so large case lists vanished: 20-60 bucket 1.7% vs 15)
                tf = card.setdefault("_tok_fail", Counter())
                tf[ncs] += 1
                tt = card.setdefault("_tok_try", Counter())
                f_ge = sum(v for x, v in tf.items() if x >= ncs)
                t_ge = sum(v for x, v in tt.items() if x >= ncs)
                if f_ge >= 4 and f_ge >= 0.5 * t_ge:
                    card["ncase_choices"] = [x for x in card["ncase_choices"] if x < ncs] or [min(card["ncase_choices"])]
            continue
        base_row = row
        held = None
        twins = []
        # relation unit (one per base)
        if unit == "neg" and eng.can_negate(spec):
            for n in (1, 2):
                s2 = eng.with_neg(spec, n)
                twins.append(("neg" if n == 1 else "dneg", s2, "complement" if n == 1 else "equiv", noop, None))
        elif unit == "inert":
            ip = eng.inert_pair(card, spec, rng, eng.labels_in(card) | ({noop[0].lower()} if noop else set()))
            if ip and spec.get("qkind") != "cases":
                twins.append(("inert", copy.deepcopy(spec), "equiv", noop, ip))
        elif unit == "attack":
            twins.append(("attack", copy.deepcopy(spec), "inv", noop, "ATTACK"))
        # own-call_id twins (label flips)
        if var == 0 and card.get("variants") and rng.random() < 0.95:
            # repair r1.1: try every flip variant (random order) before giving up (v1.0 tried one: twin sets 19.0%)
            nv = len(card["variants"])
            v0 = int(rng.random() * nv)
            for j in range(nv):
                v = 1 + (v0 + j) % nv
                s2 = eng.flip_twin(card, spec, v)
                if s2 is not None:
                    twins.append(("clause_flip", s2, None, noop, v))
                    break
        if spec.get("placement") and spec["placement"].get("near") and rng.random() < 0.9:
            s2 = eng.boundary_twin(card, spec, rng)
            if s2 is not None:
                twins.append(("boundary", s2, None, noop, None))
        for kind, s2, rel, nf, extra in twins:
            tid = f"{bid}.{kind}"
            tv = var
            inert_line = nf
            attack_line = None
            role = "clean"
            if kind == "clause_flip":
                tv = extra
            if kind == "inert":
                inert_line = extra
            if kind == "attack":
                attack_line = ATK.LINES[int(uhash("F2-atk", tid) * len(ATK.LINES))]
                role = "attacked"
            try:
                trow, tres, tP, tq = eng.to_row(card, s2, rng, row_id=tid, var=tv, eid=eid, inert=inert_line,
                                                attack=attack_line, role=role, style_key=bid)
            except Exception as e:
                out.fail["twin_render:" + type(e).__name__ + ":" + str(e)[:40]] += 1
                continue
            trow["group_id"] = bid
            trow["call_id"] = bid if rel else tid
            trow["meta"]["twin_of"] = bid
            trow["meta"]["twin_kind"] = kind
            if kind == "attack":
                if attack_line not in trow["state"] or attack_line in base_row["state"]:
                    out.fail["attack_line_accounting"] += 1
                    continue
            if emit(out, trow, tP, tres):
                if rel:
                    out.rels.append({"a": bid, "b": tid, "type": rel})
    return len(out.rows) - n0


def rank_probe(c, eng, tries=4, need=3):
    """Can this choice card put gold first and last among its ordered options? (CL and yes/no cards: yes.)"""
    if c["qtype"] == "noul" or c["schema"] == "CL":
        return True
    rng = rng_for("rank_probe", c["card_id"])
    nv = len(c.get("variants", []))
    for u in (0.0, 0.999):
        okc = 0
        for t in range(tries):
            var = (t % (nv + 1)) if nv else 0          # the build draws card variants too (held per base row)
            want = predraw(c, rng, {"neg": 0})
            want["u_rank"] = u
            if c["world"] == "open":
                want["needed"] = False
            want.pop("show_none", None)
            want["show_none"] = False
            try:
                eng.gen_row(c, rng, var, want)
                okc += 1
            except Exception:
                pass
        if okc < need:
            return False
    return True


NAMED_CYCLE = ["masked", "plain", "plain", "swapped", "masked", "plain", "masked", "swapped", "masked", "masked",
               "masked", "plain", "plain"]


def make_cards(cards, purpose):
    # repair r1.1: B1 form alternates over the cards of each sampler (v1.0 drew it per card: upper 55.7% of band rows)
    # and the named-option style cycles over the named-option cards (v1.0: masked 7.6% of choice rows, target 10-15)
    wsum = {"upper": 0.0, "lower": 0.0}
    ni = 0
    for c in cards:
        if c.get("b1") is None and (c["sampler"] == "S3" or c["schema"] == "CH-O"):
            # greedy on the expected row weight (case-list cards carry 2.2x rows), so both forms get half the rows
            side = "upper" if wsum["upper"] <= wsum["lower"] else "lower"
            c["b1"] = side
            wsum[side] += card_weight(c)           # repair r2: same weights as card_targets
        named_card = is_named_card(c)
        if named_card and "named_force" not in c:
            c["named_force"] = NAMED_CYCLE[ni % len(NAMED_CYCLE)]
            ni += 1
    made = []
    for i, c0 in enumerate(cards):
        eng = engine(SAMPLER_ENGINE[c0["sampler"]])
        pack = c0.pop("pack_obj")
        c0["short_id"] = f"F2{purpose[0]}.{c0['sampler']}.{i:02d}"
        # repair r1.1: a choice card must be able to put gold at both ends of its ordered options (R2-17: gold rank
        # uniform; 3.4: "resample, never pad"). A card whose named errors all fall on one side of gold (v1.0: 10
        # cards with gold first or last on most rows) is redrawn with a new card seed (salt), up to 11 times
        for salt in range(40):                 # repair r2: 40 card seeds (was 12; F2.S4.p4-020.CH-C failed all 12)
            c = copy.deepcopy(c0)
            rng = rng_for("card", c["card_id"]) if salt == 0 else rng_for("card", c["card_id"], salt)
            try:
                eng.make_card(c, pack, rng)
            except Exception as e:
                progress(f"card build failed {c['card_id']}: {type(e).__name__} {e}")
                raise
            c["engine"] = eng.NAME
            if rank_probe(c, eng):
                break
        c["card_salt"] = salt
        made.append(c)
    # per-card yes rates in mirrored pairs inside each sampler, so the aggregate stays near 50% (2.1)
    for s in ("S1", "S2", "S3", "S4"):
        yn = [c for c in made if c["sampler"] == s and c["qtype"] == "noul"]
        for a, b2 in zip(yn[0::2], yn[1::2]):
            b2["yes_rate"] = 1.0 - a["yes_rate"]
        if len(yn) % 2:
            # repair r1.1: the unpaired card of an odd sampler sits at 0.5, so each sampler's yes rate is 50% by
            # construction (the S2 comparator family split assumes it, A41)
            yn[-1]["yes_rate"] = 0.5
    return made


def card_record(c):
    """JSON-safe card summary for the side file."""
    keep = {k: v for k, v in c.items() if k in ("card_id", "sampler", "schema", "world", "instr", "pack", "plan",
                                                "defs_style", "dv", "short", "omitted", "wordings", "styles",
                                                "persona_seed", "yes_rate", "engine", "named", "b1", "card_salt")}
    keep["variants"] = [v["dim"] for v in c.get("variants", [])]
    keep["shown"] = sorted(c.get("shown", []))
    return json.loads(json.dumps(keep, default=str))


def run_part(cards, targets, purpose, stream, global_hashes, limit=None):
    out = Out()
    t0 = time.time()
    for i, c in enumerate(cards):
        eng = engine(c["engine"])
        rng = rng_for(stream, c["card_id"])
        tgt = targets[c["card_id"]] if limit is None else min(limit, targets[c["card_id"]])
        # repair r1.2: QC-sample rows carry their own id prefix (F2q), as in v1.0; with one card set for both parts
        # the qc rows had reused the candidate ids (F2c), which collide across the two files
        tag = None if purpose == "cand" else "F2" + purpose[0] + c["short_id"][3:]
        got = build_card_rows(c, eng, tgt, rng, out, None, purpose, global_hashes, id_tag=tag)
        if got < tgt:
            out.fail[f"short_card_rows:{c['card_id']}"] += tgt - got
        if i % 5 == 0:
            progress(f"{purpose}: card {i + 1}/{len(cards)} rows {len(out.rows)} fails {sum(out.fail.values())} "
                     f"t={time.time() - t0:.0f}s")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="cand")
    ap.add_argument("--only", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--tag", default="")
    ap.add_argument("--cards", default=None)
    ap.add_argument("--files", default=None)
    a = ap.parse_args(argv)
    only = set(a.only.split(",")) if a.only else None
    cards = make_cards(plan_cards(only), "cand")
    progress(f"cards built: {len(cards)}")
    write_json(OUT / f"cards_r1{a.tag}.json", [card_record(c) for c in cards])
    targets = card_targets(cards)
    gh = set()
    if a.part in ("cand", "all"):
        out = run_part(cards, targets, "cand", "cand", gh, a.limit)
        write_jsonl(OUT / f"candidates_r1{a.tag}.jsonl", out.rows)
        write_jsonl(OUT / f"candidates_r1{a.tag}.relations.jsonl", out.rels)
        write_json(TMP / f"cand_fail{a.tag}.json", dict(out.fail))
        progress(f"candidates: {len(out.rows)} rows, {len(out.rels)} relations, fails {dict(out.fail)}")
    if a.part in ("qc", "all"):
        qt = {k: int(round(v * 5040 / sum(targets.values()))) for k, v in targets.items()}
        out = run_part(cards, qt, "qc", "qc", gh, a.limit)
        write_jsonl(OUT / f"qc_sample{a.tag}.jsonl", out.rows)
        write_jsonl(OUT / f"qc_sample{a.tag}.relations.jsonl", out.rels)
        write_json(TMP / f"qc_fail{a.tag}.json", dict(out.fail))
        progress(f"qc sample: {len(out.rows)} rows, fails {dict(out.fail)}")
    if a.part in ("regen",):
        # v1.1: rows of the open-world cards (NEI statuses now held across retries; 2 more open cards) are rebuilt
        ids = set(a.cards.split(",")) if a.cards else {c["card_id"] for c in cards if c["world"] == "open"}
        gh |= existing_hashes()
        qt = {k: int(round(v * 5040 / sum(targets.values()))) for k, v in targets.items()}
        files = [("cand", "candidates_r1", targets, "cand"), ("qc", "qc_sample", qt, "qc")]
        if a.files:
            files = [f for f in files if f[0] in a.files.split(",")]
        for key, fname, tg, stream in files:
            run_regen(cards, tg, key, fname + a.tag, stream, gh, ids)
    if a.part in ("topup",):
        gh |= existing_hashes()
        qt = {k: int(round(v * 5040 / sum(targets.values()))) for k, v in targets.items()}
        for key, fname, tg, stream in (("cand", "candidates_r1", targets, "cand"), ("qc", "qc_sample", qt, "qc")):
            run_topup(cards, tg, key, fname + a.tag, stream, gh)
    if a.part in ("dev", "all"):
        if a.part == "dev":
            gh |= existing_hashes()
            progress(f"dev: {len(gh)} training structure hashes loaded (dev items must be disjoint)")
        out = run_mixdev(gh)
        write_jsonl(OUT / f"mixdev_S5{a.tag}.jsonl", out.rows)
        write_json(TMP / f"dev_fail{a.tag}.json", dict(out.fail))
        progress(f"mixdev: {len(out.rows)} items, fails {dict(out.fail)}")
    if a.part in ("g4s5", "all"):
        if a.part == "g4s5":
            gh |= existing_hashes()
        main_g4s5(train_hashes=gh)
    write_json(TMP / f"structure_hashes{a.tag}.json", sorted(gh))
    return 0



def existing_hashes():
    """Structure hashes of every row already written to the training-side files (candidates, QC sample)."""
    from .common import read_jsonl
    hs = set()
    for fn in ("candidates_r1.jsonl", "qc_sample.jsonl"):
        p = OUT / fn
        if p.exists():
            hs |= {r["meta"]["structure_hash"] for r in read_jsonl(p)}
    return hs


def qc_ids(rows, rels):
    """QC-sample ids start "F2q." (v1.0 wrote them with the candidates' "F2c." prefix, so the two files shared ids;
    ids never appear in row text, so this is a pure relabel of id, group_id, call_id, twin_of and relation ends)."""
    f = lambda x: ("F2q." + x[4:]) if isinstance(x, str) and x.startswith("F2c.") else x  # noqa: E731
    for r in rows:
        for k in ("id", "group_id", "call_id"):
            r[k] = f(r[k])
        r["meta"]["twin_of"] = f(r["meta"].get("twin_of"))
    for x in rels:
        x["a"], x["b"] = f(x["a"]), f(x["b"])
    return rows, rels


def run_regen(cards, targets, key, fname, stream, gh, card_ids):
    """Drop every row (and relation) of the named cards from a written file and rebuild them to the card targets on a
    fresh RNG stream, with base numbers from 7000 (no id clash with the first pass)."""
    from .common import read_jsonl
    path, relp = OUT / f"{fname}.jsonl", OUT / f"{fname}.relations.jsonl"
    rows, rels = read_jsonl(path), read_jsonl(relp)
    if key == "qc":
        rows, rels = qc_ids(rows, rels)
    drop = {r["id"] for r in rows if r["meta"]["card_id"] in card_ids}
    rows = [r for r in rows if r["id"] not in drop]
    rels = [x for x in rels if x["a"] not in drop and x["b"] not in drop]
    progress(f"{key} regen: dropped {len(drop)} rows of {len(card_ids)} cards")
    out = Out()
    t0 = time.time()
    for c in cards:
        if c["card_id"] not in card_ids:
            continue
        eng = engine(c["engine"])
        rng = rng_for(stream + "_regen", c["card_id"])
        n0 = len(out.rows)
        build_card_rows(c, eng, targets[c["card_id"]], rng, out, None, key, gh, nb_start=7000,
                        id_tag=c["short_id"].replace("F2c.", "F2q.", 1) if key == "qc" else None)
        progress(f"{key} regen: {c['card_id']} {len(out.rows) - n0}/{targets[c['card_id']]} t={time.time() - t0:.0f}s")
    ids_seen = {r["id"] for r in rows}
    dup = [r["id"] for r in out.rows if r["id"] in ids_seen]
    if dup:
        raise SystemExit(f"regen id collision: {dup[:5]}")
    rows += out.rows
    rels += out.rels
    write_jsonl(path, rows)
    write_jsonl(relp, rels)
    write_json(TMP / f"{key}_regen_fail.json", dict(out.fail))
    progress(f"{key} regen: +{len(out.rows)} rows, total {len(rows)}, fails {dict(out.fail)}")


def run_topup(cards, targets, key, fname, stream, gh):
    """Top a written file up to its target (sum of card targets): first the cards below their own target, then, for a
    sampler still below its budget, its other cards in order of fewest rows (each <= 128). New rows use a fresh RNG
    stream and base numbers from 20500, so ids never collide with the first pass."""
    from .common import read_jsonl
    path, relp = OUT / f"{fname}.jsonl", OUT / f"{fname}.relations.jsonl"
    rows, rels = read_jsonl(path), read_jsonl(relp)
    if key == "qc":
        rows, rels = qc_ids(rows, rels)
    have = Counter(r["meta"]["card_id"] for r in rows)
    out = Out()
    t0 = time.time()
    by_s = defaultdict(list)
    for c in cards:
        by_s[c["sampler"]].append(c)
    ids_seen = {r["id"] for r in rows}
    rnd = Counter()

    def one(c, n):
        rnd[c["card_id"]] += 1
        eng = engine(c["engine"])
        rng = rng_for(stream + "_topup", c["card_id"], rnd[c["card_id"]])
        n0 = len(out.rows)
        build_card_rows(c, eng, n, rng, out, None, key, gh, nb_start=20000 + 500 * rnd[c["card_id"]],
                        id_tag=c["short_id"].replace("F2c.", "F2q.", 1) if key == "qc" else None,
                        deadline=time.time() + 150)
        got = len(out.rows) - n0
        have[c["card_id"]] += got
        return got

    for c in cards:
        short = targets[c["card_id"]] - have[c["card_id"]]
        if short > 0:
            got = one(c, short)
            progress(f"{key} topup: {c['card_id']} short {short} got {got} t={time.time() - t0:.0f}s")
    for s, cs in sorted(by_s.items()):
        need = sum(targets[c["card_id"]] for c in cs) - sum(have[c["card_id"]] for c in cs)
        tries = 0
        while need > 0 and tries < 3 * len(cs):
            tries += 1
            c = min((c for c in cs if have[c["card_id"]] < 120), key=lambda c: (have[c["card_id"]], c["card_id"]),
                    default=None)
            if c is None:
                break
            got = one(c, min(need, 8))
            need -= got
            if got == 0:
                have[c["card_id"]] += 1000       # skip a card that cannot give more
        progress(f"{key} topup: sampler {s} remaining need {max(need, 0)}")
    dup = [r["id"] for r in out.rows if r["id"] in ids_seen]
    if dup:
        raise SystemExit(f"topup id collision: {dup[:5]}")
    rows += out.rows
    rels += out.rels
    write_jsonl(path, rows)
    write_jsonl(relp, rels)
    write_json(TMP / f"{key}_topup_fail.json", dict(out.fail))
    progress(f"{key} topup: +{len(out.rows)} rows, total {len(rows)}, fails {dict(out.fail)}")


# ----------------------------------------------------------------------------------------------------------------- mix-tuning dev

SWEEP_CARDS = {
    # sampler -> level -> card configs that reach exactly that many unstated operations (no printed intermediates)
    "S1": {1: [dict(schema="YN-T", plan="unit", nlines=1, with_add=False, partial=False, nexc=0),
               dict(schema="CH-V", plan="pct", nexc=1)],
           2: [dict(schema="YN-T", plan="unit", nlines=1, with_add=True, partial=False, nexc=1),
               dict(schema="CH-V", plan="disc", with_add=True, nexc=1)],
           3: [dict(schema="YN-T", plan="unit", nlines=2, with_add=False, partial=False, nexc=0),
               dict(schema="CH-V", plan="net", nlines=2, nded=2, nexc=0)],
           4: [dict(schema="YN-T", plan="unit", nlines=2, with_add=True, partial=False, nexc=0),
               dict(schema="CH-V", plan="unit", nlines=2, with_add=True, partial=False, nexc=0)],
           5: [dict(schema="YN-T", plan="unit_fee", nlines=2, partial=False, nexc=0),
               dict(schema="CH-V", plan="unit_fee", nlines=2, partial=False, nexc=0)]},
    "S2": {1: [dict(schema="YN-T", plan="min", nexc=1), dict(schema="CH-V", plan="disc_min", nexc=1)],
           2: [dict(schema="YN-T", plan="unit", nlines=1, with_add=True, partial=False, nexc=1),
               dict(schema="CH-V", plan="net", nlines=2, nded=1, nexc=0)],
           3: [dict(schema="YN-T", plan="unit_fee", nlines=1, partial=False, nexc=1),
               dict(schema="CH-V", plan="unit", nlines=2, with_add=False, partial=False, nexc=0)],
           4: [dict(schema="YN-T", plan="unit", nlines=2, with_add=True, partial=False, nexc=0),
               dict(schema="CH-V", plan="unit", nlines=2, with_add=True, partial=False, nexc=0)],
           5: [dict(schema="YN-T", plan="unit_fee", nlines=2, partial=False, nexc=0),
               dict(schema="CH-V", plan="unit_fee", nlines=2, partial=False, nexc=0)]},
    "S3": {1: [dict(schema="YN-T", rate_kind="pct", b2="flat", fee=False, computed=False),
               dict(schema="CH-V", rate_kind="pct", b2="flat", fee=False, computed=False)],
           2: [dict(schema="YN-T", rate_kind="pct", b2="flat", fee=True), dict(schema="CH-B")],
           3: [dict(schema="YN-T", rate_kind="unit", b2="flat", fee=True), dict(schema="CH-V", rate_kind="pct", b2="flat", fee=True)],
           4: [dict(schema="YN-T", rate_kind="pct", b2="marginal", fee=False), dict(schema="CH-V", rate_kind="pct", b2="marginal", fee=False)],
           5: [dict(schema="YN-T", rate_kind="pct", b2="marginal", fee=True), dict(schema="CH-V", rate_kind="pct", b2="marginal", fee=True)]},
    "S4": {1: [dict(schema="YN-D", rule_kind="cal", no_ext=True), dict(schema="CH-D", rule_kind="cal", no_ext=True)],
           2: [dict(schema="YN-D", rule_kind="cal", force_ext=True, ext_unit="cal"), dict(schema="CH-O", rule_kind="cal")],
           3: [dict(schema="YN-D", rule_kind="bday", force_ext=True, ext_unit="cal"),
               dict(schema="CH-O", rule_kind="cal", force_ext=True, ext_unit="cal")],
           4: [dict(schema="YN-D", rule_kind="bday", force_ext=True, ext_unit="bday", ext_k=12),
               dict(schema="CH-O", rule_kind="bday", force_ext=True, ext_unit="cal")],
           5: [dict(schema="YN-D", rule_kind="bday", force_ext=True, ext_unit="bday", ext_k=12),
               dict(schema="CH-O", rule_kind="bday", force_ext=True, ext_unit="bday", ext_k=12),
               dict(schema="CH-O", rule_kind="bday", force_ext=True, ext_unit="bday", ext_k=12)]},
    "S5": {1: [dict(schema="CH-D"), dict(schema="CH-D")],
           2: [dict(schema="YN-T", no_deds=True, no_b4=True), dict(schema="CH-V", no_deds=True, no_b4=True)],
           3: [dict(schema="YN-T", no_deds=True, no_b4=True), dict(schema="CH-V", no_deds=True, no_b4=True)],
           4: [dict(schema="YN-T", no_deds=True, no_b4=True), dict(schema="CH-V", no_deds=True, no_b4=True)],
           5: [dict(schema="YN-T", no_deds=True, no_b4=True), dict(schema="CH-V", no_deds=True, no_b4=True)]},
}


def _dev_card(sampler, cfg, pack, i, tag):
    sch = cfg["schema"]
    if sampler == "S5" and sch in ("CH-V", "CH-D"):
        # v1.1: S5 choice cards carry no deduction lines and no B4 split (their card text, printed twice by the
        # layout, left most rows at >= 1,900 tokens); S5 YN-T cards keep both
        cfg = {**cfg, "no_deds": True, "no_b4": True}
    cid = f"F2.{sampler}.{pack['id']}.{sch}.{tag}{i}"
    c = {"card_id": cid, "sampler": sampler, "schema": sch, "world": "closed", "instr": "std", "held_out": True}
    c.update({k: v for k, v in cfg.items() if k != "schema"})
    eng = engine(SAMPLER_ENGINE[sampler])
    rng = rng_for("devcard", cid)
    eng.make_card(c, pack, rng)
    c["engine"] = eng.NAME
    c["short_id"] = f"F2{tag}.{sampler}.{i:02d}"
    return c


def run_mixdev(global_hashes):
    out = Out()
    tr, he = packs.split()
    cards = []
    # 400 S5 items: 20 held-out cards x 20 (YN-T 10, CH-V 5, CH-D 5)
    s5 = []
    for i in range(20):
        sch = "YN-T" if i < 10 else ("CH-V" if i < 15 else "CH-D")
        s5.append(_dev_card("S5", {"schema": sch}, he[i % len(he)], i, "dev"))
    def s5_rows(c, need):
        eng = engine(c["engine"])
        rng = rng_for("dev", c["card_id"])
        used = set()
        n = 0
        tries = 0
        while n < need and tries < 400:
            tries += 1
            want = {"neg": 0}
            if c["qtype"] == "noul":
                want["aff"] = (n % 2 == 0)
            try:
                spec = eng.gen_row(c, rng, 0, want)
            except Reject:
                continue
            h = canon.structure_hash(canon.canonize(spec["LP"]))
            if h in global_hashes:
                continue
            spec["tf"] = rng.random() < 0.5
            rid = f"{c['short_id']}.{n:04d}"
            try:
                row, res, P, q = eng.to_row(c, spec, rng, row_id=rid, eid=eng.new_eid(c, rng, used))
            except Exception as e:
                out.fail["dev_render:" + type(e).__name__] += 1
                continue
            row["group_id"] = row["call_id"] = rid
            row["meta"]["mixdev"] = "S5"
            if emit(out, row, P, res):
                global_hashes.add(h)
                n += 1
        return n

    # v1.1: a card that cannot give its 20 items passes its shortfall to an extra held-out card of the same schema
    deficit = Counter()
    for c in s5:
        n = s5_rows(c, 20)
        if n < 20:
            out.fail[f"dev_short:{c['card_id']}"] += 20 - n
            deficit[c["schema"]] += 20 - n
    xi = 40
    for sch in sorted(deficit):
        for _ in range(6):
            if deficit[sch] <= 0:
                break
            c = _dev_card("S5", {"schema": sch}, he[xi % len(he)], xi, "dev")
            xi += 1
            deficit[sch] -= s5_rows(c, deficit[sch])
        if deficit[sch] > 0:
            out.fail[f"dev_unfilled:{sch}"] += deficit[sch]
    progress(f"mixdev S5: {len(out.rows)} items")
    # depth sweep: 5 levels x S1-S5 x 12 (6 yes/no with 3 yes + 6 choice where the level has a choice card)
    short = Counter()
    hi = 20
    for level in range(1, 6):
        for s in ("S1", "S2", "S3", "S4", "S5"):
            cfgs = SWEEP_CARDS[s][level]
            cs = []
            for j, cfg in enumerate(cfgs):
                try:
                    cs.append(_dev_card(s, cfg, he[(hi + j) % len(he)], level * 10 + j, "sw"))
                except Exception as e:
                    progress(f"sweep card failed {s} L{level} {cfg}: {type(e).__name__} {e}")
            hi += len(cfgs)
            want_items = [("yn", True)] * 3 + [("yn", False)] * 3 + [("ch", None)] * 6
            got = 0
            for extra in range(4):
                if extra:
                    # v1.1: items a level's cards could not give are tried on the same configs on other held-out packs
                    cs = []
                    for j, cfg in enumerate(cfgs):
                        try:
                            cs.append(_dev_card(s, cfg, he[(hi + 97 * extra + j) % len(he)], level * 10 + j, f"sx{extra}"))
                        except Exception as e:
                            progress(f"sweep extra card failed {s} L{level} {cfg}: {type(e).__name__} {e}")
                yn = [c for c in cs if c["qtype"] == "noul"]
                ch = [c for c in cs if c["qtype"] == "choice"]
                failed = []
                for kind, aff in want_items:
                    if not try_sweep_item(s, level, kind, aff, yn, ch, got, out, global_hashes):
                        failed.append((kind, aff))
                    else:
                        got += 1
                want_items = failed
                if not want_items:
                    break
            short[(s, level)] += len(want_items)
            progress(f"sweep L{level} {s}: {got}/12")
    out.fail.update({f"sweep_short:{k[0]}:L{k[1]}": v for k, v in short.items() if v})
    return out


def try_sweep_item(s, level, kind, aff, yn, ch, got, out, global_hashes):
    """One sweep item of the wanted kind (yes/no with a given affirmative truth value, or choice); yes/no falls back to
    the level's choice cards when no yes/no card reaches the level, and the other way round."""
    pools = [yn, ch] if kind == "yn" else [ch, yn]
    ok = False
    for pool in pools:
        if ok or not pool:
            continue
        for attempt in range(40):
            c = pool[attempt % len(pool)]
            eng = engine(c["engine"])
            rng = rng_for("sweep", c["card_id"], level, got, attempt, kind)
            want = {"neg": 0, "sweep": level} if s != "S5" else {"neg": 0, "sweep_depth": level}
            if c["qtype"] == "noul" and aff is not None:
                want["aff"] = aff
            try:
                spec = eng.gen_row(c, rng, 0, want)
            except Reject:
                continue
            if spec.get("printed") or spec.get("ops") != level:
                continue
            h = canon.structure_hash(canon.canonize(spec["LP"]))
            if h in global_hashes:
                continue
            spec["tf"] = rng.random() < 0.5
            rid = f"F2sw.{s}.L{level}.{got:02d}"
            try:
                row, res, P, q = eng.to_row(c, spec, rng, row_id=rid, eid=eng.new_eid(c, rng, set()))
            except Exception:
                continue
            row["group_id"] = row["call_id"] = rid
            row["meta"]["mixdev"] = "sweep"
            row["meta"]["sweep_level"] = level
            if emit(out, row, P, res):
                global_hashes.add(h)
                ok = True
                break
    return ok


def main_dev(tag=""):
    gh = set()
    out = run_mixdev(gh)
    write_jsonl(OUT / f"mixdev_S5{tag}.jsonl", out.rows)
    write_json(TMP / f"dev_fail{tag}.json", dict(out.fail))
    progress(f"mixdev: {len(out.rows)} items, fails {dict(out.fail)}")
    return out


def main_g4s5(n=1000, train_hashes=None):
    """Extra S5 rows for the G4 metamorphic run only (S5 has 460 dev items; G4 needs >= 1,000 rows per generator).
    Written to tmp/, never an output."""
    out = Out()
    tr, he = packs.split()
    gh = set()
    i = 0
    while len(out.rows) < n and i < 200:
        sch = ["YN-T", "CH-V", "CH-D", "YN-T"][i % 4]
        c = _dev_card("S5", {"schema": sch}, he[(i * 7) % len(he)], i, "g4")
        eng = engine("stmt")
        rng = rng_for("g4s5", c["card_id"])
        used = set()
        for j in range(12):
            try:
                spec = eng.gen_row(c, rng, 0, {"neg": rng.choice([0, 0, 1, 2]) if c["qtype"] == "noul" else 0})
            except Reject:
                continue
            spec["tf"] = True
            rid = f"F2g4.S5.{i:03d}.{j:02d}"
            try:
                row, res, P, q = eng.to_row(c, spec, rng, row_id=rid, eid=eng.new_eid(c, rng, used))
            except Exception:
                continue
            row["group_id"] = row["call_id"] = rid
            emit(out, row, P, res)
        i += 1
    write_jsonl(TMP / "g4_s5_rows.jsonl", out.rows)
    progress(f"G4 S5 extra rows: {len(out.rows)} (tmp only), fails {dict(out.fail)}")
    return out


if __name__ == "__main__":
    sys.exit(main())
