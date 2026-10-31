"""F3 round-1 build: candidate pool, G6 QC sample and S5 mix-tuning dev items.

  python build.py --part candidates|qc|dev [--workers 8] [--cards F3-c001,...] [--scale 1.0]

Every row is labelled by solver A, re-derived by solver B (G2), by solver C on open cards, rendered through fmt1
(render_row_text + loader_check, G15 per-row part), parsed back by parse_f3 (G3; checks 1-8), counted with the real
tokenizer on the served prompt (instructions printed twice) and with the shared negcount. A row that fails any check is
a generator bug: it is logged (counts per reason) and the build reports it; nothing is silently relabelled.
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import multiprocessing as mp
import os
import random
import re
import subprocess
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import cards as CARDS  # noqa: E402
import questions as QS  # noqa: E402
import render_f3 as RF  # noqa: E402
import solver_a as A  # noqa: E402
import solver_b as B  # noqa: E402
import solver_c as C  # noqa: E402
import textforms as TF  # noqa: E402
from f3common import (C_SRC, FAMILY, GEN_VERSION, LEAN, LICENCE, OUT, ROLE_VALUE, SOURCE, SPEC_ID, TMP, log_progress,
                      rng_for, unit_hash)
from samplers import SAMPLERS, draw_bin, make_open  # noqa: E402

sys.path.insert(0, str(C_SRC / "common"))
import negcount  # noqa: E402

QT_TARGET = {"Q1": 0.16, "Q2": 0.15, "Q3": 0.15, "Q4": 0.22, "Q5": 0.12, "Q6": 0.05, "Q7": 0.10, "Q8": 0.05}
P_NEG, P_D, P_FLIP, P_PREM, P_ATTACK, P_INERT = 0.28, 0.55, 0.36, 0.20, 0.40, 0.25
K_CANDS = 10
NEG_W = {"N1": 0.35, "N2": 0.2, "N3": 0.2, "N4": 0.15, "N5": 0.2}
ROUND1_ROWS = 4500
CAND_ROWS = 9000   # repair r2: 2x of 4,500, so the G10 target cells (depth d3-d4, 20-60 options, 25-40 entries) keep a surplus after G9

_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from transformers import AutoTokenizer
        _TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    return _TOK


def served_tokens(row):
    """Real-tokenizer length of the served prompt (chat template, cygnet system, schema_branch_mark user message)."""
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    try:
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        if row.get("options") and len(row["options"]) > len(dio.WIDE):
            U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            dio.WIDE = list(U) + [a + b for a in U for b in U]
        r = dict(row)
        user = dio.user_msg(r, None)
        text = dio.render_chat(tokenizer(), dio.CYGNET_SYSTEM, user)
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved
    return len(tokenizer()(text)["input_ids"])


def git_sha():
    try:
        return subprocess.check_output(["git", "-C", str(LEAN), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


GIT_SHA = None


# ------------------------------------------------------------------------------------------------ QT planning

def qt_probs(cards, n_rows):
    """Per-card QT probabilities by iterative proportional fitting toward the family shares (+/- 3 pp)."""
    p = {}
    for c in cards:
        qs = c["qts"]
        if c.get("theme"):
            prim = qs[0]
            p[c["card_id"]] = {q: (0.85 if q == prim else 0.15 / max(1, len(qs) - 1)) for q in qs}
            if len(qs) == 1:
                p[c["card_id"]] = {prim: 1.0}
            continue
        p[c["card_id"]] = {q: 1.0 / len(qs) for q in qs}
    tot = sum(n_rows[c["card_id"]] for c in cards)
    for _ in range(0 if all(c.get("theme") for c in cards) else 80):
        share = collections.Counter()
        for c in cards:
            for q, v in p[c["card_id"]].items():
                share[q] += v * n_rows[c["card_id"]] / tot
        for c in cards:
            pc = p[c["card_id"]]
            for q in pc:
                if share[q] > 0:
                    pc[q] *= (QT_TARGET[q] / share[q]) ** 0.5
            z = sum(pc.values())
            for q in pc:
                pc[q] /= z
    for c in cards:
        if c["vocab"] in ("masked", "swapped"):
            pc = p[c["card_id"]]
            for q in pc:
                pc[q] *= 1.5 if q in ("Q1", "Q2") else 1.0
            z = sum(pc.values())
            for q in pc:
                pc[q] /= z
    return p


# ------------------------------------------------------------------------------------------------ row assembly

class Gen:
    def __init__(self, card, purpose, n_rows, probs, seed_tag, parser=True, id_prefix=None):
        self.c = card
        self.id_prefix = id_prefix if id_prefix is not None else \
            {"candidates": "c1.", "qc": "q1.", "dev": "d1.", "test": "t."}.get(purpose, purpose + ".")
        self.purpose = purpose
        self.n_rows = n_rows
        self.probs = probs
        self.rng = rng_for("rows", purpose, seed_tag, card["card_id"])
        self.rows, self.rels, self.side = [], [], []
        self.fail = collections.Counter()
        self.skips = collections.Counter()
        self.alt_log = collections.Counter()
        self.bucket_n = collections.Counter()
        self.log_no = 0
        self.base_yn = 0
        self.base_yes = 0
        self.pending = {}
        self.abs_exp = collections.Counter()
        self.abs_got = collections.Counter()
        self.qt_n = collections.Counter()
        self.depth_n = collections.Counter()
        self.dec_n = collections.Counter()
        self.mech_n = collections.Counter()
        self.mech_pres = collections.Counter()
        self.mech_dec = collections.Counter()
        self.mech_lab = collections.Counter()
        self.bin_n = collections.Counter()
        # repair r2.2: per-bin length-redraw failures (a bin no log of this card fits is dropped from its plan, G11
        # rows per card); per-question-type base yes/no tallies (labels follow the drawn rate inside each question
        # type, G7 Q3 / per-card drawn rate); per-card yes/no tallies of negated (k_all >= 1) rows by wording cell
        # (G10 yes rate per wording x k_all cell)
        self.bin_fail = collections.Counter()
        self.base_qt = collections.defaultdict(lambda: [0, 0])
        self.kcell = collections.defaultdict(lambda: [0, 0])
        self.kidx = collections.Counter()
        # repair3 (G10 yes rate per wording x k_all cell; G6/G7 wording x label skews): negated (k_all >= 1) yes/no
        # rows are emitted as yes/no pairs per (card, k_all bucket, wording). kpend[(kb, label)]: twin rows already
        # built and checked but not yet emitted, waiting for a partner of the other label (a partner renders in the
        # waiting row's wording; both are then emitted; twins still waiting when the card ends are never emitted).
        # kopen[(kb, label)]: emitted base rows with k_all >= 1 (comparator stems) waiting for a twin partner.
        self.kpend = collections.defaultdict(list)
        self.kopen = collections.defaultdict(list)
        # repair3 (G7 primary null: base rows ~ Bernoulli(drawn rate); PLAIN base rows ran yes-heavy): per-card
        # base-row label tallies per decisive mechanism, steered to the card's drawn rate
        self.mech_lab_b = collections.Counter()
        # repair3 (visible stem-form cue: Q4 "still" base rows ran 71/96 yes vs 51 expected from the drawn rates):
        # per-card base-row label tallies per stem form (question type, stem kind, point kind, "still")
        self.form_lab_b = collections.Counter()
        self.pl = collections.Counter()
        self.n_rows_made = 0
        self.yes_all = 0
        self.yn_all = 0
        self.lg_obs = 0.0      # choice rows: gold among the longest options (observed vs expected n_longest / k)
        self.lg_exp = 0.0
        self.lenlog = []
        self.parser = parser
        self.hashes = set()
        self.illus = None
        self.fewshot = None
        crng = rng_for("cardtext", card["card_id"])
        if card["def_style"] == "one_line_examples":
            self.illus = RF.illustrations(card, crng)
        if card.get("fewshot"):
            self.fewshot = RF.fewshot_block(card, crng)

    # ---------------------------------------------------------------- plan
    def plan(self):
        rng, c = self.rng, self.c
        # repair r2 (G10 event bins 30/40/30): the bin is chosen by the card's deficit against a card-level target,
        # so a log lost to the 1,900-token redraw is re-planned in the same bin (section 6: a redraw keeps its bin)
        # instead of drifting to short logs. Full choice cards print their rules twice and cannot fit 25+ entries;
        # yes/no and 2.1 cards carry the 25-40 bin.
        if c.get("form_mode") == "choice" and c["rule21"] is None:
            tgt = (0.45, 0.55, 0.0)
        elif c["rule21"] is not None:
            tgt = (0.22, 0.33, 0.45)
        else:
            tgt = (0.12, 0.26, 0.62)
        tot = sum(self.bin_n.values()) + 3
        w = [max(0.0, t - self.bin_n[i] / tot + 0.05) if t > 0 else 0.0 for i, t in enumerate(tgt)]
        # repair r2.2 (G11: S6 choice cards starved at 3 rows): a bin where this card's logs keep failing the
        # 1,900-token cap (>= 30 redraws, under 1 kept row per 20) is dropped from the card's plan
        w = [0.0 if self.bin_fail[i] >= 30 and self.bin_n[i] * 20 < self.bin_fail[i] else x for i, x in enumerate(w)]
        if sum(w) <= 0:
            w = [1.0, 0.0, 0.0]
        bi = rng.choices([0, 1, 2], weights=w)[0]
        if bi == 2:
            n = rng.randint(25, 27) if rng.random() < 0.85 else rng.randint(28, 32)
            if c["encoding"] in ("table", "rec"):
                n = rng.randint(25, 26)
        elif bi == 1:
            n = rng.randint(13, 24) if c.get("form_mode") != "choice" else rng.randint(13, 18)
        else:
            n = rng.randint(5, 12)
        if c["inverted"]:
            bi, n = (0, rng.randint(5, 12)) if rng.random() < 0.6 else (1, rng.randint(13, 15))
        plan = {"bin": bi, "n_entries": n}
        plan["chains"] = self.plan_chains(bi)
        if c.get("form_mode") == "choice" or c["encoding"] in ("table", "rec"):
            plan["n_items"] = rng.randint(2, 6)
            plan["n_holders"] = rng.randint(3, 7)
        if bi == 2:
            plan["n_items"] = rng.randint(3, 5)
            plan["n_holders"] = rng.randint(3, 5)
        if c["world"] == "open" and not c["inverted"]:
            # the open hide (make_open) removes 1-2 entries or a leading extract; plan a little longer so the shown
            # log stays in the planned bin
            plan["n_entries"] = min(40, plan["n_entries"] + (4 if c["gap_style"] == "leading" else 2))
        c["_bin_lo"] = (5, 13, 25)[bi]
        if c.get("deep_card"):
            plan["deep_layers"] = rng.choice([0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6])
        if c["sampler"] == "S2":
            plan["decile"] = rng.randrange(10)
            ms = ["plain"] + [m for m in ("VOID", "CORR", "SUPERSEDE", "RENAME", "MERGE", "CHECK") if m in c["mechs"]]
            plan["mech"] = rng.choice(ms)
        # option-count buckets: large rosters for Q5 / Q7 rows
        want = self.want_bucket()
        plan["want_bucket"] = want
        if want >= 2 and set(c["qts"]) & {"Q5", "Q7"}:
            if c["sampler"] == "S3" or c["inverted"]:
                plan["n_items" if "Q7" in c["qts"] else "n_holders"] = rng.randint(11, 16) if want == 2 \
                    else rng.randint(21, 25)
            else:
                plan["n_holders"] = rng.randint(11, 15) if want == 2 else rng.randint(20, 23)
            plan["n_entries"] = rng.randint(5, 9) if want == 3 else rng.randint(5, 12)
            plan["bin"] = 0
            plan["big_roster"] = True
        return plan

    def plan_chains(self, bi):
        """Repair r2: planted decisive chains for this log (logbuild.set_windows): 1-3 items, the field each chain
        writes (status for Q1/Q2, holder for Q4-Q8, by the card's question-type probabilities) and its planned depth,
        drawn by the card's running depth deficit (queries on chain items carry the d2-d4 share; other items give
        mostly d1 rows)."""
        rng, c = self.rng, self.c
        ps = sum(v for q, v in self.probs.items() if q in ("Q1", "Q2"))
        ph = sum(v for q, v in self.probs.items() if q in ("Q4", "Q5", "Q6", "Q7", "Q8"))
        k = rng.choice([2, 2, 3]) if bi == 0 else rng.choice([2, 3, 3, 4])
        tot = sum(self.depth_n.values()) or 1
        T = {1: 0.06, 2: 0.20, 3: 0.30, 4: 0.32, 5: 0.12}
        w = [max(0.02, T[d] + 0.5 * ((0.15, 0.30, 0.30, 0.25, 0.07)[d - 1] - self.depth_n[d] / tot)) for d in T]
        out = []
        for _ in range(k):
            field = "status" if rng.random() < ps / max(1e-9, ps + ph) else "holder"
            out.append((field, rng.choices(list(T), weights=w)[0]))
        return out

    def want_bucket(self):
        """Option-count bucket for this log's choice rows. Q5 / Q7 rows (holders, items) carry the 10-19 and 20-60
        buckets for the family, so cards themed on them lean large; status, record rows stay at 2-9 (10-19 for
        records)."""
        c = self.c
        if c.get("lean_roster"):
            target = (0.03, 0.05, 0.12, 0.80)
        elif c.get("theme") == "Q7":
            target = (0.25, 0.40, 0.30, 0.05)
        elif c.get("theme") in ("Q5", "Q7", "Q5o"):
            target = (0.10, 0.20, 0.32, 0.38)
        elif c.get("theme") == "Q3":
            target = (0.45, 0.45, 0.10, 0.0)
        else:
            target = (0.5, 0.5, 0.0, 0.0)
        tot = sum(self.bucket_n.values()) or 1
        w = [max(0.01, t - self.bucket_n[i] / tot + 0.03) if t > 0 else 0.0 for i, t in enumerate(target)]
        return self.rng.choices(range(4), weights=w)[0]

    # ---------------------------------------------------------------- run
    def run(self):
        c = self.c
        guard = 0
        while len(self.rows) < self.n_rows and guard < self.n_rows * 14:
            guard += 1
            try:
                self.one_log()
            except Exception as ex:  # a generator bug must be visible
                self.fail["exception:" + type(ex).__name__] += 1
                if self.fail["exception:" + type(ex).__name__] <= 3:
                    sys.stderr.write(f"[{c['card_id']}] {traceback.format_exc()[-1500:]}\n")
        # repair3: twins still waiting for a partner of the other label were never emitted (counted, not written)
        for k, lst in self.kpend.items():
            self.skips[f"kpair_unemitted_kb{k[0]}"] += len(lst)
        for k, lst in self.kopen.items():
            self.skips[f"kpair_open_base_kb{k[0]}"] += len(lst)
        self.kpend.clear()
        return self

    def _kstate(self, kb, lab):
        """repair3 pairing state for a negated row of label `lab` in k_all bucket kb: (completes a waiting partner,
        number of same-label rows already waiting)."""
        return (bool(self.kpend[(kb, 1 - lab)] or self.kopen[(kb, 1 - lab)]),
                len(self.kpend[(kb, lab)]) + len(self.kopen[(kb, lab)]))

    @staticmethod
    def _kwait(n_wait):
        return 1.0 if n_wait == 0 else 0.45 if n_wait == 1 else 0.12

    def one_log(self):
        c, rng = self.c, self.rng
        plan = self.plan()
        self._cur_bin = plan["bin"]
        c["_big_roster_now"] = bool(plan.get("big_roster"))
        b = SAMPLERS[c["sampler"]](c, rng, plan)
        c["_big_roster_now"] = False
        if b.n < 5:
            self.skips["short_log"] += 1
            return
        S = b.S
        full = None
        if c["world"] == "open":
            got = make_open(c, b, rng)
            if not got:
                self.skips["open_hide_failed"] += 1
                return
            S, full = got
        self.log_no += 1
        log_id = f"{self.id_prefix}{c['card_id']}-L{self.log_no:03d}"
        S["_log_id"] = log_id
        if getattr(b, "target_item", None):
            S["_target"] = b.target_item
        S["_focus"] = list(getattr(b, "win", {}) or [])
        S["_fdocs"] = list(getattr(b, "dwin", {}) or [])
        RF.set_listing(c, S, rng)
        c["_doctype"] = dict(b.doc_type)
        roles = {}
        for h in b.holders + [e.get("new") for e in S["entries"] if e["t"] == "RENAME" and e["kind"] == "holder"]:
            if h:
                roles[h] = rng.choice(c["roles"])[0]
        notes = {}
        if c["notes_on"] and c["inert"] and rng.random() < P_INERT and c["encoding"] != "git" and plan["bin"] < 2:
            for e in rng.sample(S["entries"], min(2, len(S["entries"]))):
                notes[e["n"] if c["encoding"] != "notice" else e["n"]] = rng.choice(c["inert"])
            if c["encoding"] == "notice":
                notes = {("notice", S["entries"][0]["ref"]): rng.choice(c["inert"])}
        n_base = rng.randint(2, 4)
        made = 0
        ctx = QS.Ctx(c, S) if S["world"] == "closed" else None
        tg = self.toggles(S)
        for j in range(n_base * 4):
            if made >= n_base or len(self.rows) >= self.n_rows:
                break
            qt = self.pick_qt()
            cands, seen = [], set()
            for k in range(K_CANDS):
                spec = self.draw_spec(S, ctx, roles, plan, qt=qt)
                if not spec:
                    continue
                h = canon.structure_hash(S, tg, spec["Q"])
                if h in self.hashes or h in seen:
                    self.skips["dup_hash"] += 1
                    continue
                seen.add(h)
                try:
                    _, info = B.solve(S, spec["Q"])
                except AssertionError:
                    continue
                cands.append((self.score(spec, info, S), k, spec, info))
            if not cands:
                continue
            cands.sort(key=lambda x: (-x[0], x[1]))
            spec = cands[0][2]
            if not self.accept(cands[0][3], qt=spec["Q"].get("qt"), spec=spec):
                self.skips["accept_reject"] += 1
                continue
            unit = self.build_unit(S, full, spec, notes, roles, log_id, made)
            if unit:
                made += 1

    # ---------------------------------------------------------------- stratified acceptance (section 5, R1-13)
    def pick_qt(self):
        rng = self.rng
        tot = sum(self.qt_n.values()) or 1
        w = {q: max(0.01, p - self.qt_n[q] / tot + 0.04) for q, p in self.probs.items()}
        qs = list(w)
        return rng.choices(qs, weights=[w[q] for q in qs])[0]

    def accept(self, info, qt=None, spec=None):
        """Stratified acceptance (S1 sheet: queries are enumerated and kept so the section 5 targets hold; repair r2):
        the best candidate of a draw is kept with lower probability when its depth bucket or decisive decile is
        already over the card's target share (rows are rejected before they exist; nothing is relabelled)."""
        tot = sum(self.depth_n.values())
        if tot < 6:
            return True
        tq = sum(self.qt_n.values())
        if qt is not None and tq >= 6 and self.qt_n[qt] / tq < self.probs.get(qt, 0) - 0.03:
            return True        # a question type under its share is never held back (QT shares +/- 3 pp)
        if spec is not None and spec["Q"].get("form") == "yn" and spec.get("gold") in (0, 1) and self.base_yn >= 4:
            # a base yes/no row whose label the card still needs is never held back (R2-05: base rows follow the
            # drawn rate); depth and label can correlate inside a question type
            gap = self.c["yes_rate"] - self.base_yes / self.base_yn
            qy, qn = self.base_qt[spec["Q"].get("qt")]
            if qn >= 4:   # repair r2.2: the label the question type still needs
                gap = self.c["yes_rate"] - qy / qn
            if (spec["gold"] == 1 and gap > 0.02) or (spec["gold"] == 0 and gap < -0.02):
                return True
        db = min(info["depth"], 5)
        T = {1: 0.15, 2: 0.29, 3: 0.29, 4: 0.23, 5: 0.07}
        p = 1.0
        over = self.depth_n[db] / tot - T[db]
        if over > 0.04:
            p *= 0.2 if over > 0.12 else 0.45
        dec = info.get("decile")
        dt = sum(self.dec_n.values())
        if dec is not None and dt >= 10 and self.dec_n[dec] / dt > 0.13:
            p *= 0.5
        return self.rng.random() < p

    def score(self, spec, info, S):
        """Prefer the candidate query that best fills the F3 targets (section 5; repair r2 adds the label-aware
        terms): the non-deep depth mix (d1 15, d2 30, d3 30, d4 25; deep <= 10%), uniform decisive deciles, each
        mechanism decisive on >= 8% of rows, each present mechanism decisive on about 50% of the rows where it
        appears, and a 50% yes rate per decisive mechanism. All tallies are per card, so the family and per-sampler
        aggregates follow."""
        d = info["depth"]
        db = min(d, 5)
        tot = sum(self.depth_n.values()) or 1
        dtarget = {1: 0.14, 2: 0.28, 3: 0.28, 4: 0.23, 5: 0.07}
        sc = 6.0 * (dtarget[db] - self.depth_n[db] / tot)
        dec = info.get("decile")
        if dec is not None:
            dt = sum(self.dec_n.values()) or 1
            sc += 4.0 * (0.1 - self.dec_n[dec] / dt)
        mt = max(1, self.n_rows_made)
        path = mech_on_path(info, S)
        for m in path:
            sc += 3.0 * max(0.0, 0.13 - self.mech_n[m] / mt)
        for m in mech_present(S, self.c, info):
            pres = self.mech_pres[m]
            r = self.mech_dec[m] / pres if pres else 0.5
            sc += 2.0 * ((0.5 - r) if m in path else (r - 0.5))
        g = spec.get("gold")
        if spec["Q"].get("form") == "yn" and g in (0, 1):
            # repair3 (G7 primary null, base rows ~ Bernoulli(the card's drawn rate): base rows with no decisive
            # mechanism (PLAIN) ran 677 yes vs 596 expected): score() ranks base candidates, so each decisive
            # mechanism's (PLAIN included) base-row yes share is steered to the card's drawn rate, not to 50%;
            # cards' drawn rates average near 50%, so the family per-mechanism yes rate stays near 50%
            # Tallied per (question type, mechanism): in Q8 a PLAIN path means the transfer took effect (yes by
            # T38) and in Q3 a PLAIN path mostly means the record is current, so a yes candidate of those types is
            # steered to a path with a non-blocking mechanism when the draw offers one (no label is changed)
            pd = self.c["yes_rate"]
            qt0 = spec["Q"].get("qt")
            for m in path:
                n_m = self.mech_lab_b[(qt0, m, 0)] + self.mech_lab_b[(qt0, m, 1)]
                r = (self.mech_lab_b[(qt0, m, 1)] + 2 * pd) / (n_m + 2)
                sc += 3.0 * ((pd - r) if g == 1 else (r - pd))
            fk = _stem_form(spec["Q"])
            n_f = self.form_lab_b[(fk, 0)] + self.form_lab_b[(fk, 1)]
            r = (self.form_lab_b[(fk, 1)] + 2 * pd) / (n_f + 2)
            sc += 3.0 * ((pd - r) if g == 1 else (r - pd))
            # repair r2.2 (G6 (d) metadata / G7: 'yes = bad outcome' polarity and present mechanisms carried the
            # label): among same-label candidates prefer the polarity / present mechanisms that label lacks
            for f in _pl_feats(spec, S, self.c, info):
                a1, a0 = self.pl[(f, 1)], self.pl[(f, 0)]
                sc += 3.0 * ((a0 - a1) if g == 1 else (a1 - a0)) / (a0 + a1 + 6)
        if spec["Q"].get("form") == "choice" and spec.get("options"):
            # "longest option is gold" within +/- 2 pp of the tie-aware chance (G10): steer by the card's running
            # excess (observed minus expected)
            o, e = _longest_terms(spec["options"], spec.get("gold"))
            dev = self.lg_obs - self.lg_exp
            sc += 0.6 * max(-3.0, min(3.0, -dev)) * (o - e)
        if S.get("_target") and spec["Q"].get("item") and A.Ents(S).find(spec["Q"]["item"]) == \
                A.Ents(S).find(S["_target"]):
            sc += 0.15
        return sc + 0.02 * self.rng.random()

    # ---------------------------------------------------------------- query draw
    def draw_spec(self, S, ctx, roles, plan, qt=None):
        c, rng = self.c, self.rng
        probs = self.probs
        qs = list(probs)
        if qt is None:
            qt = rng.choices(qs, weights=[probs[q] for q in qs])[0]
        long_log = plan.get("bin") == 2
        if long_log and qt in ("Q5", "Q7") and rng.random() < 0.7 and len(qs) > 1:
            return None
        cm = 0.35 if long_log else 1.25
        if c.get("form_mode") == "choice":
            cm = 100.0
        elif c.get("form_mode") == "yn":
            cm = 0.0
        # per-card yes rate on base yes/no rows (R2-05): follow the drawn rate by deficit, not by coin
        n_b, y_b = self.base_yn, self.base_yes
        target = 1 if (y_b + 0.5) / (n_b + 1) < c["yes_rate"] else 0
        # repair r2.2 (G7: Q3 yes/no rows 29% yes against drawn 58%; one card's Q8 rows 27-40% against 74%): the
        # deficit is followed inside each question type once it has 2 base rows, so no question type drifts to the
        # label its queries reach most easily
        qy, qn = self.base_qt[qt]
        if qn >= 2:
            target = 1 if (qy + 0.5) / (qn + 1) < c["yes_rate"] else 0
        # repair r2: was 0.1; r2.2: no flip while the question type is more than 5 pp off the drawn rate (a label
        # its queries rarely reach otherwise drifts to the flip by repeated tries)
        rate_q = (qy / qn) if qn >= 2 else ((y_b / n_b) if n_b else c["yes_rate"])
        if rng.random() < 0.03 and abs(rate_q - c["yes_rate"]) < 0.05:
            target = 1 - target
        wb = plan.get("want_bucket")
        if S["world"] == "open":
            if qt == "Q1":
                form = "choice" if rng.random() < cm * (0.75 if c["vocab"] != "plain" else 0.4) else "yn"
            elif qt == "Q5":
                form = "choice"
            else:
                form = "yn"
            if qt == "Q1" and form == "yn" and c.get("form_mode") == "choice":
                return None
            if form == "choice":
                n_h = len({x[1] for x in S["register"]["items"]} | {e[k] for e in S["entries"]
                                                                       for k in ("holder", "sender", "receiver")
                                                                       if e.get(k)})
                slot = self.abstain_slot(("open", qt), wb, len(S["statuses"]) + 1 if qt == "Q1" else n_h + 1)
                spec = QS.open_query(c, S, rng, qt, form, target=target, roles=roles, slot=slot)
                return self.settle(("open", qt), spec)
            return QS.open_query(c, S, rng, qt, form, target=target, roles=roles)
        if qt == "Q1":
            if c["has_qty"] and rng.random() < 0.25 and c.get("form_mode") != "choice":
                return QS.q_qty(ctx, rng, target=target)
            form = "choice" if rng.random() < cm * (0.8 if c["vocab"] != "plain" else 0.45) else "yn"
            return QS.q_status(ctx, rng, form=form, target=target, want_bucket=min(wb, 1) if form == "choice" else None)
        if qt == "Q2":
            if not c.get("q2_on"):
                return None
            r = rng.random()
            if r < 0.25 and c.get("form_mode") != "choice":
                pt = QS.range_point(ctx, rng)
                if not pt:
                    return None
                if c["has_qty"] and rng.random() < 0.3:
                    return QS.q_qty(ctx, rng, target=target, point=pt)
                return QS.q_status(ctx, rng, form="yn", target=target, point=pt)
            pt = QS.date_point(ctx, rng)
            if not pt:
                return None
            if c["has_qty"] and r > 0.85 and c.get("form_mode") != "choice":
                return QS.q_qty(ctx, rng, target=target, point=pt)
            form = "choice" if rng.random() < cm * (0.8 if c["vocab"] != "plain" else 0.45) else "yn"
            return QS.q_status(ctx, rng, form=form, target=target, point=pt,
                               want_bucket=min(wb, 1) if form == "choice" else None)
        if qt == "Q3":
            form = "choice" if rng.random() < cm * 0.5 else "yn"
            return QS.q_record(ctx, rng, form=form, target=target, want_bucket=min(wb, 2) if form == "choice" else None)
        if qt == "Q4" and c.get("deep_card") and S.get("_target") and rng.random() < 0.85:
            return QS.q_holds(ctx, rng, target=target, roles=roles, mode="end", item=S["_target"])
        if qt == "Q4":
            r = rng.random()
            mode = "end" if r < 0.5 else ("still" if r < 0.7 else "date")
            if mode == "still" and (S["sampler"] == "S6" or not c.get("still_on")):
                mode = "end"
            if mode == "date" and not c.get("q2_on"):
                mode = "end"
            return QS.q_holds(ctx, rng, target=target, roles=roles, mode=mode)
        if qt == "Q5":
            return QS.q_who(ctx, rng, want_bucket=wb)
        if qt == "Q6":
            return QS.q_count(ctx, rng, target=target, roles=roles)
        if qt == "Q7":
            slot = self.abstain_slot(("Q7",), max(wb, 0), len(ctx.item_latest) + 1, k_min=3)
            return self.settle(("Q7",), QS.q_inverse(ctx, rng, slot=slot))
        if qt == "Q8":
            return QS.q_transfer(ctx, rng, target=target, roles=roles)
        return None

    # ---------------------------------------------------------------- display-then-gold (XF01)
    def abstain_slot(self, key, want_bucket, k_cap, k_min=2):
        """The (k, abstain-gold) slot for a row that may show an abstain option (XF01 display-then-gold). k comes
        from the wanted bucket; the gold slot is the abstain option with frequency exactly 1/k: a per-(option,
        bucket) running balance (expected sum of 1/k vs abstain golds emitted) decides the class, and the class is
        kept until a structure matches it (structures are rejected, never relabelled), so the realised abstain-gold
        share is 1/k within each bucket by construction."""
        rng = self.rng
        lo, hi = QS.BUCKETS[want_bucket if want_bucket is not None else 0]
        hi = min(hi, k_cap, 30 if want_bucket != 3 else 23)   # repair r2: 20-60 rows near 20 options (token cap)
        lo = max(lo, k_min)
        if lo > hi:
            lo, hi = max(k_min, 2), max(k_min, min(4, k_cap))
        k = rng.randint(lo, hi)
        if k < 3:
            return {"k": k, "abstain_gold": False}
        opt = "None" if key == ("Q7",) else "NEI"
        bk = 0 if k <= 4 else 1 if k <= 9 else 2 if k <= 19 else 3
        exp = self.abs_exp[(opt, bk)] + 1.0 / k
        return {"k": k, "abstain_gold": exp - self.abs_got[(opt, bk)] > 0.5}

    def settle(self, key, spec):
        return spec

    # ---------------------------------------------------------------- units and twins
    def build_unit(self, S, full, spec, notes, roles, log_id, u):
        c, rng = self.c, self.rng
        call_id = f"{log_id}-U{u:02d}"
        base_id = f"{call_id}-a"
        if c["rule21"]:
            ok, why = QS.alt_check(c, S, spec["Q"], spec["gold"])
            if not ok:
                self.alt_log["drop:" + "+".join(why)] += 1
                return False
            self.alt_log["keep"] += 1
        base = self.make_row(S, spec, notes, base_id, call_id, log_id, twin_of=None, twin_kind=None, full=full)
        if base is None:
            return False
        unit_rows = [base]
        Q = spec["Q"]
        # negation twins (complement / equiv), same call_id
        p_neg = {"S3": 0.6, "S2": 0.48, "S4": 0.34, "S6": 0.34}.get(c["sampler"], P_NEG)
        # repair r2 (G7/G8; spec 8 G7 "fix by matched twins first"): label-flip twins go more often to base rows
        # with the card's majority label, so a card's yes/no rows as a whole sit nearer 50% while its base rows keep
        # the drawn rate (R2-05); pack words then carry no label signal. Weights only; no label is changed.
        tw = 1.0
        if Q["form"] == "yn" and spec["gold"] in (0, 1):
            # steer by the card's yes share over all its yes/no rows so far (twins included), so each card's
            # rows, and the pool as a whole, sit near 50%
            r_all = (self.yes_all + 0.5) / (self.yn_all + 1)
            bias = min(0.9, 1.6 * abs(c["yes_rate"] - 0.5) + 3.0 * abs(r_all - 0.5))
            maj = (1 if r_all > 0.5 else 0) if abs(r_all - 0.5) > 0.02 else (1 if c["yes_rate"] > 0.5 else 0)
            tw = (1.0 + bias) if spec["gold"] == maj else (1.0 - bias)
        # repair3 (G10 wording x k_all cells; replaces the r2.2 kf weights): negated rows are emitted in yes/no
        # pairs per k_all bucket (make_row). A negation twin (k_all 1) carries the flipped label, a double negation
        # (k_all 2) the base label; a twin that completes a waiting partner is drawn at 0.95, one that would wait is
        # drawn at the sampler rate, less when same-label rows already wait (so few twins end the card unemitted)
        p_d = 0.75 if c["sampler"] == "S3" else P_D
        if Q["form"] == "yn" and spec["gold"] in (0, 1):
            g0 = int(spec["gold"])
            comp1, wait1 = self._kstate(1, 1 - g0)
            comp2, wait2 = self._kstate(2, g0)
            p_neg = 0.95 if comp1 else min(0.95, p_neg * self._kwait(wait1))
            p_d = 0.95 if comp2 else min(0.95, p_d * self._kwait(wait2))
        else:
            comp1 = comp2 = False
        # the unit gate also opens for a double negation that completes a waiting k_all-2 partner; the negation twin
        # then keeps its own rate (p_neg / p_gate inside the gate)
        p_gate = max(p_neg, p_d if comp2 else 0.0)
        if Q["form"] == "yn" and c["neg_on"] and rng.random() < p_gate and Q.get("neg", "A") == "A":
            forms, dkind = QS.neg_forms_allowed(Q)
            if not c.get("still_on"):
                forms = [f for f in forms if f != "N2"]
                dkind = {"N1N2": "N1", "N2": None}.get(dkind, dkind)
            if "N2" in forms and not self._guard(S, Q):
                forms = [f for f in forms if f != "N2"]
                dkind = {"N1N2": "N1", "N2": None}.get(dkind, dkind)
            if forms:
                w = dict(NEG_W)
                if Q["kind"] in ("qty", "count"):
                    w["N4"] = 0.6
                f = rng.choices(forms, weights=[w[x] for x in forms])[0]
                tq = QS.twin_neg(Q, f)
                ts = dict(spec, Q=tq, gold=A.answer(S, tq), polarity=_flip_pol(spec.get("polarity")))
                make_neg = comp1 or rng.random() < p_neg / max(p_gate, 1e-9)
                if make_neg and ts["gold"] in (0, 1) and ts["gold"] == 1 - spec["gold"] and \
                        self._alt_ok(S, tq, ts["gold"]):
                    r = self.make_row(S, ts, notes, f"{call_id}-n", call_id, log_id, twin_of=base_id,
                                      twin_kind="neg", full=full, rel=(base_id, "complement"))
                    if r:
                        unit_rows.append(r)
                if dkind and rng.random() < p_d:
                    opts = {"N1": ["N1"], "N2": ["N2"], "N1N2": ["N1", "N2"], "N1N3": ["N1", "N3"]}[dkind]
                    db = rng.choice(opts)
                    if db == "N2" and not (Q.get("still") or (Q["qt"] == "Q4" and Q["point"]["kind"] == "end")):
                        db = "N1"
                    if db == "N2" and not self._guard(S, Q):
                        db = None
                    if db:
                        dq = QS.twin_neg(Q, "D", db)
                        ds = dict(spec, Q=dq, gold=A.answer(S, dq))
                        if ds["gold"] == spec["gold"] and self._alt_ok(S, dq, ds["gold"]):
                            r = self.make_row(S, ds, notes, f"{call_id}-d", call_id, log_id, twin_of=base_id,
                                              twin_kind="dneg", full=full, rel=(base_id, "equiv"))
                            if r:
                                unit_rows.append(r)
        # contrast twins (own call_id): fact flip or premise removal
        rr = rng.random() / tw if tw > 0 else 1.0
        if rr < P_FLIP + P_PREM:
            order = ["fact_flip", "premise_removal"] if rr < P_FLIP else ["premise_removal", "fact_flip"]
            for kind in order:
                if self.contrast_twin(S, full, spec, notes, base, log_id, u, kind):
                    break
        # attack twin (inv), same call_id, only when the unit stays <= 3 rows
        if len(unit_rows) <= 2 and c["notes_on"] and rng.random() < P_ATTACK and c["encoding"] != "git":
            an = dict(notes)
            import registry as R
            txt = rng.choice(R.ATTACK)
            if c["encoding"] == "notice":
                an = {("notice", rng.choice(S["notices"])["ref"]): txt}
            else:
                an = {rng.choice(S["entries"])["n"]: txt}
            self.make_row(S, spec, an, f"{call_id}-x", call_id, log_id, twin_of=base_id, twin_kind="attack",
                          full=full, attack=True, rel=(base_id, "inv"))
        return True

    def stated(self):
        c = self.c
        if c["def_style"] == "none":
            return []
        if c["def_style"] == "short":
            return CARDS.short_card_rules(c)[0]
        return CARDS.stated_rules(c)

    def toggles(self, S):
        return canon.row_toggles(self.c, S, self.stated())

    def _guard(self, S, Q):
        if S["world"] == "open":
            vals, eff, E = A.open_values(S)
            return A.open_guard(S, Q, eff, E)
        states, eff, E, _ = A.replay(S)
        return A.guard_ok(S, states, eff, E, Q["item"], Q["holder"])

    def _alt_ok(self, S, Q, gold):
        if not self.c["rule21"]:
            return True
        ok, why = QS.alt_check(self.c, S, Q, gold)
        self.alt_log[("keep" if ok else "drop:" + "+".join(why))] += 1
        return ok

    def contrast_twin(self, S, full, spec, notes, base, log_id, u, kind):
        """A label-flip twin (XF03): fact flip (void or change an entry on the decisive path) or premise removal
        (delete a writer on the path; A42). Closed cards only (open premise removal is not generated). The twin is
        kept only if solvers A and B both give a different label. Returns True when a twin row was made."""
        c, rng = self.c, self.rng
        Q = spec["Q"]
        info = base["_info"]
        if S["world"] == "open":
            return False
        path = [n for n in reversed(info.get("path") or []) if n is not None]
        if info.get("decisive") is not None:
            path = [info["decisive"]] + [n for n in path if n != info["decisive"]]
        for dec in path[:4]:
            S2 = mutate(S, dec, kind, rng, c)
            if S2 is None or A.check_rules(S2):
                self.skips[f"{kind}_invalid"] += 1
                continue
            try:
                ok = _query_valid(S2, Q)
            except Exception:
                ok = False
            if not ok:
                continue
            lab = A.answer(S2, Q)
            if lab in (None, A.UNK, A.NO_SINGLE) or lab == spec["gold"]:
                self.skips[f"{kind}_no_flip"] += 1
                continue
            if Q["form"] == "choice" and Q["qt"] == "Q5":
                lab = A.latest_id(S2, None, lab)
            if Q["form"] == "choice" and lab not in (spec.get("options") or []):
                continue
            ids2 = struct_ids(S2)
            qids = [Q.get(k) for k in ("item", "holder", "record") if Q.get(k)] + list(Q.get("candidates") or [])
            if any(x not in ids2 for x in qids) or any(
                    re.fullmatch(r"[A-Z]{2,4}-[0-9A-Z]{2,5}", o) and o not in ids2 for o in (spec.get("options") or [])):
                self.skips[f"{kind}_ids_gone"] += 1
                continue
            if not self._alt_ok(S2, Q, lab):
                continue
            ts = dict(spec, gold=lab, polarity=spec.get("polarity"))
            cid = f"{log_id}-U{u:02d}{'f' if kind == 'fact_flip' else 'p'}"
            S2["_log_id"] = S["_log_id"]
            RF.set_listing(c, S2, rng)
            r = self.make_row(S2, ts, {}, f"{cid}-a", cid, log_id, twin_of=base["id"], twin_kind=kind, full=None)
            if r is not None:
                return True
        return False

    # ---------------------------------------------------------------- one row
    def make_row(self, S, spec, notes, rid, call_id, log_id, *, twin_of, twin_kind, full=None, attack=False,
                 rel=None):
        c = self.c
        Q = spec["Q"]
        gold = spec["gold"]
        # G2: solver B on the generator's structure
        try:
            lb, info = B.solve(S, Q)
        except AssertionError as ex:
            self.fail["solverB_assert"] += 1
            return None
        if S["world"] == "open":
            if lb == B.UNKNOWN:
                lb = c["nei"] if Q["form"] == "choice" else "UNK"
            elif Q["form"] == "choice" and Q["qt"] == "Q5":
                lb = A.latest_id(S, None, lb)
        elif Q["form"] == "choice" and Q["qt"] == "Q5":
            lb = A.latest_id(S, None, lb)
        if lb != gold:
            self.fail["G2_A_vs_B"] += 1
            return None
        if S["world"] == "open":
            vc = C.verify(S, Q, gold, nei=c["nei"], full=full)
            if not vc["ok"]:
                self.fail["solverC:" + vc["why"]] += 1
                return None
        depth = info["depth"]
        n_adj = sum(1 for n in info["path"] if any(e["n"] == n and e["t"] == "ADJUST" for e in S["entries"]))
        deep = depth >= 5 or n_adj >= 3 or bool(spec.get("q6_deep"))
        if depth > 8:
            self.skips["depth_cap"] += 1
            return None
        kneg = expected_neg(Q)[1]
        wid_pick = None
        kkey = partner = None
        if Q["form"] == "yn" and kneg >= 1 and gold in (0, 1):
            # repair3 (G10 yes rate per wording x k_all cell): a negated row whose other-label partner is waiting
            # (a deferred twin or an emitted comparator base row of this card and k_all bucket) renders in the
            # partner's wording, so the two enter the same wording cell as a yes/no pair
            kb = min(kneg, 3)
            kkey = (kb, int(gold))
            for kind in ("pend", "open"):
                lst = (self.kpend if kind == "pend" else self.kopen)[(kb, 1 - int(gold))]
                if lst:
                    partner = (kind, lst[0])
                    wid_pick = lst[0]["wid"]
                    break
        try:
            fields, res, st, wid, cir, question, tok = RF.render_row(c, S, spec, notes, row_key=rid, illus=self.illus,
                                                                      fewshot=self.fewshot, measure=served_tokens,
                                                                      wid=wid_pick)
        except RF.LengthError as ex:
            self.skips["redraw_len_ge_1900"] += 1
            self.skips[f"redraw_len_bin{getattr(self, '_cur_bin', '?')}_{Q['form']}"] += 1
            if isinstance(getattr(self, "_cur_bin", None), int):
                self.bin_fail[self._cur_bin] += 1
            self.lenlog.append((Q["form"], str(ex)))
            return None
        except Exception as ex:
            self.fail["render:" + str(ex)[:60]] += 1
            return None
        qtype = "choice" if Q["form"] == "choice" else "noul"
        nc = negcount.count(question)
        exp = expected_neg(Q)
        if (nc.k_syn, nc.k_all) != exp:
            self.fail["negcount_form_mismatch"] += 1
            return None
        tg = self.toggles(S)
        h = canon.structure_hash(S, tg, Q)
        if h in self.hashes and twin_kind != "attack":
            self.skips["dup_hash"] += 1
            return None
        row = {"id": rid, "group_id": log_id, "call_id": call_id, "source": SOURCE, "state": fields["state"],
               "qtype": qtype, "instructions": fields["instructions"],
               "options": list(spec["options"]) if qtype == "choice" else None,
               "gold": gold if qtype == "choice" else int(gold), "role": ROLE_VALUE, "card": fields["card"]}
        n_events = len([e for e in S["entries"] if not (e["t"] == "VOID" and e.get("_withdraw"))])
        meta = {"family": FAMILY, "spec_id": SPEC_ID, "card_id": c["card_id"], "domain_pack": c["pack_id"],
                "sampler": c["sampler"], "gen_version": GEN_VERSION, "git_sha": GIT_SHA,
                "seed": int(unit_hash("seed", rid) * 2 ** 31), "structure_hash": h, "difficulty_bin": None,
                "crowd_pg": None, "depth": depth, "deep": deep, "format_style": st["id"], "wording_id": wid,
                "defs_style": c["def_style"], "twin_of": twin_of, "twin_kind": twin_kind, "text_source": None,
                "licence": LICENCE, "edge": edge_tags(c, spec, attack), "persona_seed": c["persona_seed"]}
        row["meta"] = meta
        if self.parser:
            import parse_f3 as P
            pr = P.check_row(row, c, expect={"S": S, "Q": Q, "gold": gold, "toggles": tg,
                                              "hash": h, "options": spec.get("options"), "neg": exp})
            if not pr["ok"]:
                self.fail["G3:" + pr["why"][:70]] += 1
                return None
        row["_info"] = info

        def commit():
            self.hashes.add(h)
            if twin_of is None and qtype == "noul":
                self.form_lab_b[(_stem_form(Q), int(gold))] += 1
                self.base_yn += 1
                self.base_yes += int(gold) == 1
                self.base_qt[Q["qt"]][0] += int(gold) == 1
                self.base_qt[Q["qt"]][1] += 1
            if qtype == "noul" and kneg >= 1:
                self.kcell[(wid, min(kneg, 3))][int(gold) == 1] += 1
                self.kidx[(min(kneg, 3), int(gold))] += 1
            if twin_of is None:
                self.qt_n[Q["qt"]] += 1
            self.depth_n[min(depth, 5)] += 1
            if info.get("decile") is not None:
                self.dec_n[info["decile"]] += 1
            mech = mech_on_path(info, S)
            for m in mech:
                self.mech_n[m] += 1
                if qtype == "noul":
                    self.mech_lab[(m, int(gold))] += 1
                    if twin_of is None:
                        self.mech_lab_b[(Q["qt"], m, int(gold))] += 1
            for m in mech_present(S, c, info):
                self.mech_pres[m] += 1
                self.mech_dec[m] += m in mech
            if qtype == "noul":
                for f in _pl_feats(spec, S, c, info):
                    self.pl[(f, int(gold))] += 1
            self.n_rows_made += 1
            if qtype == "noul":
                self.yn_all += 1
                self.yes_all += int(gold) == 1
            else:
                o, e = _longest_terms(spec["options"], gold)
                self.lg_obs += o
                self.lg_exp += e
            self.bin_n[_bin_of(n_events)] += 1
            side = {"id": rid, "world": S["world"], "stated_toggles": CARDS.stated_rules(c) if not c["rule21"] else
                    ("short:" + ",".join(CARDS.short_card_rules(c)[0]) if c["rule21"] == "short" else "none"),
                    "n_events": n_events, "event_bin": _bin_of(n_events), "decisive_decile": info.get("decile"),
                    "mechanisms": mech, "mech_present": mech_present(S, c, info), "qt": Q["qt"],
                    "polarity": spec.get("polarity"), "polarity_source": "pack_or_hash_tag",
                    "inverted_card": c["inverted"], "status_option_row": bool(spec.get("status_option_row")),
                    "vocab": c["vocab"], "neg_form": Q.get("neg", "A") if qtype == "noul" else None, "dbase": Q.get("dbase"),
                    "k_syn": nc.k_syn, "k_all": nc.k_all, "real_tokens": tok, "leak_key": canon.leak_key(
                        S, tg, Q), "k_options": len(spec["options"]) if qtype == "choice" else 2,
                    "abstain": spec.get("abstain"), "gold_is_abstain": gold in (c["nei"], c["none"]),
                    "rule21": c["rule21"], "yes": (int(gold) if qtype == "noul" else None), "deep": deep, "depth": depth,
                    "gold_letter": res["gold_letter"], "card_yes_rate": c["yes_rate"], "point": (Q.get("point") or {}).get(
                        "kind"), "still": bool(Q.get("still")), "listing": c["listing"], "encoding": c["encoding"],
                    "container": st["container"], "attack": attack, "planned_mech": c.get("_planned_mech")}
            if os.environ.get("F3_DEBUG_DUMP"):
                side["_dbg"] = {"S": S, "Q": Q, "toggles": tg, "hash": h, "options": spec.get("options"),
                                "neg": list(exp), "card_id": c["card_id"]}
            self.rows.append(row)
            self.side.append(side)
            if qtype == "choice":
                k = len(spec["options"])
                self.bucket_n[0 if k <= 4 else 1 if k <= 9 else 2 if k <= 19 else 3] += 1
                if spec.get("abstain"):
                    bk = 0 if k <= 4 else 1 if k <= 9 else 2 if k <= 19 else 3
                    self.abs_exp[(spec["abstain"], bk)] += 1.0 / k
                    self.abs_got[(spec["abstain"], bk)] += int(gold in (c["nei"], c["none"]))
            if rel is not None:
                self.rels.append({"a": rel[0], "b": rid, "type": rel[1]})

        if kkey is None:
            commit()
        elif partner is not None and wid == partner[1]["wid"]:
            # repair3: this row completes a waiting partner of the other label (same card, k_all bucket, wording)
            commit()
            kind, ent = partner
            (self.kpend if kind == "pend" else self.kopen)[(kkey[0], 1 - kkey[1])].pop(0)
            if kind == "pend":
                ent["commit"]()
            self.skips[f"kpair_pairs_kb{kkey[0]}"] += 1
        elif twin_of is not None:
            # repair3: a twin with no partner waits (built and checked, not emitted); its structure hash is held
            self.hashes.add(h)
            self.kpend[kkey].append({"wid": wid, "commit": commit, "id": rid})
            self.skips[f"kpair_wait_kb{kkey[0]}"] += 1
        else:
            commit()
            self.kopen[kkey].append({"wid": wid, "id": rid})
        return row


def struct_ids(S):
    ids = set()
    for it in S["register"]["items"]:
        ids.add(it[0]); ids.add(it[1])
    for d, r in S["register"].get("docs", []):
        ids.add(r)
    for e in S["entries"]:
        for k in ("item", "holder", "sender", "receiver", "old", "new", "absorbed", "survivor", "record"):
            if isinstance(e.get(k), str):
                ids.add(e[k])
        if e["t"] == "CORR" and e["slot"] == "receiver":
            ids.add(e["value"])
    return ids


def _bin_of(n):
    return 0 if n <= 12 else 1 if n <= 24 else 2


def _flip_pol(p):
    return None if p is None else ("not bad" if p == "bad" else "bad")


def edge_tags(c, spec, attack):
    tags = []
    if c["vocab"] != "plain" and spec.get("status_option_row"):
        tags.append(c["vocab"])
    if c["inverted"]:
        tags.append("inverted")
    if c.get("fewshot"):
        tags.append("fewshot")
    if c["rule21"]:
        tags.append("rule21:" + c["rule21"])
    if attack:
        tags.append("attack")
    if c["world"] == "open":
        tags.append("open:" + c["gap_style"])
    return tags


def expected_neg(Q):
    """(k_syn, k_all) the 2.2 form table gives for this stem."""
    form = Q.get("neg", "A")
    cmp_ = Q.get("cmp")
    comp = 1 if cmp_ in ("no fewer than", "no more than") else 0
    if Q["form"] == "choice":
        return (0, 0)
    if form == "A":
        return (0, comp)
    if form in ("N1", "N2", "N4"):
        return (1, 1)
    if form in ("N3", "N5"):
        return (0, 1)
    if form == "D":
        return (2, 2) if Q.get("dbase") in ("N1", "N2") else (1, 2)
    raise ValueError(form)


def _stem_form(Q):
    """repair3: the visible stem form of a yes/no query (question type, stem kind, point kind, 'still')."""
    return (Q.get("qt"), Q.get("kind"), (Q.get("point") or {}).get("kind"), bool(Q.get("still")))


def _longest_terms(options, gold):
    """(gold is among the longest options, expected share n_longest / k) for one choice row."""
    lens = [len(o) for o in options]
    mx = max(lens)
    n_max = sum(1 for x in lens if x == mx)
    return (1.0 if gold in options and len(gold) == mx else 0.0), n_max / len(options)


def mech_on_path(info, S):
    """Decisive mechanisms (R2-11). The transfer conditions are decisive only when a stated condition blocks a
    transfer on the decisive path (repair r2: solver B's CHECK tag marks every checked transfer; CHECKBLOCK marks
    a blocked one)."""
    m = set(info.get("mech") or [])
    out = []
    for k in ("VOID", "CORRECTION", "SUPERSEDE", "RENAME", "MERGE"):
        if k in m:
            out.append(k)
    if "CHECKBLOCK" in m:
        out.append("CHECK")
    if not out:
        out.append("PLAIN")
    return out


def _pl_feats(spec, S, c, info):
    """Row features whose yes rate is balanced per card (repair r2.2): polarity tag and present mechanisms."""
    pol = spec.get("polarity")
    return ([("pol", pol)] if pol else []) + [("mp", m) for m in sorted(mech_present(S, c, info))]


def mech_present(S, c, info=None):
    """Mechanisms present on a row (R2-11). An entry mechanism appears when the log has an entry of that type. The
    transfer conditions appear when the card states T18, T19 or T40 AND the decisive path contains a transfer
    (G0 section 5; repair r2: the check used to count every log with a transfer, so status rows on check cards
    counted it as present but inert)."""
    ts = {e["t"] for e in S["entries"]}
    out = []
    if ts & {"VOID", "WITHDRAW"}:
        out.append("VOID")
    if "CORR" in ts:
        out.append("CORRECTION")
    for k in ("SUPERSEDE", "RENAME", "MERGE"):
        if k in ts:
            out.append(k)
    if (c["check"] or c["lock"]) and "TRANSFER" in ts:
        if info is None:
            out.append("CHECK")
        else:
            path = set(n for n in (info.get("path") or []) if n is not None)
            if "CHECK" in (info.get("mech") or []) or any(e["t"] == "TRANSFER" and e["n"] in path
                                                            for e in S["entries"]):
                out.append("CHECK")
    return out


def _query_valid(S, Q):
    """Rule 15 on a twin structure: every item the question names exists at its query point."""
    states, eff, E, _ = A.replay(S)
    pt = Q.get("point") or {"kind": "end"}
    if Q["qt"] in ("Q3", "Q8", "Q6"):
        if Q["qt"] == "Q8":
            return any(e["n"] == Q["entry"] and e["t"] == "TRANSFER" for e in S["entries"])
        return True
    if Q["qt"] == "Q7":
        return all(E.find(x) in states[-1].exists for x in Q["candidates"])
    if pt["kind"] == "range":
        idx = sum(1 for e in eff if A.entry_date(S, e) < pt["d1"])
    elif pt["kind"] == "end":
        idx = len(eff)
    else:
        idx = A.point_index(S, eff, pt)
    if E.find(Q["item"]) not in states[idx].exists:
        return False
    if Q.get("still") or Q.get("neg") == "N2" or (Q.get("neg") == "D" and Q.get("dbase") == "N2"):
        return A.guard_ok(S, states, eff, E, Q["item"], Q["holder"])
    return True


def mutate(S, dec, kind, rng, c):
    """Fact flip (void / change the decisive entry) or premise removal (delete it and renumber; A42)."""
    S2 = copy.deepcopy(S)
    tgt = next((e for e in S2["entries"] if e["n"] == dec), None)
    if tgt is None:
        return None
    if kind == "fact_flip":
        r = rng.random()
        if tgt["t"] in ("SET", "ADJUST", "TRANSFER", "SUPERSEDE", "CORR") and r < 0.5 and S2["sampler"] != "S4":
            last = S2["entries"][-1]
            e = {"t": "VOID", "target": dec, "n": last["n"] + 1, "date": last["date"], "time": last.get("time")}
            if S2["sampler"] == "S6":
                e["date"] = last["date"]
            S2["entries"].append(e)
            return S2
        if tgt["t"] == "SET" and tgt["field"] == "status":
            tgt["value"] = rng.choice([s for s in S2["statuses"] if s != tgt["value"]])
            return S2
        if tgt["t"] == "TRANSFER":
            hs = sorted({e["receiver"] for e in S2["entries"] if e["t"] == "TRANSFER"} |
                        {x[1] for x in S2["register"]["items"]})
            hs = [h for h in hs if h not in (tgt["receiver"], tgt["sender"])]
            if not hs:
                return None
            tgt["receiver"] = rng.choice(hs)
            return S2
        if tgt["t"] == "CORR" and tgt["slot"] == "value" and isinstance(tgt["value"], str):
            tgt["value"] = rng.choice([s for s in S2["statuses"] if s != tgt["value"]])
            return S2
        if tgt["t"] == "SET" and tgt["field"] == "qty":
            tgt["value"] = max(0, tgt["value"] + rng.choice((-7, -4, 4, 7)))
            return S2
        return None
    # premise removal (closed): delete the writer, the VOID / CORRECTION entries that name it, renumber
    if tgt["t"] in ("CREATE", "OPEN", "RENAME") or S2["sampler"] == "S4":
        return None
    gone = {dec} | {e["n"] for e in S2["entries"] if e["t"] in ("VOID", "CORR") and e.get("target") == dec}
    keep = [e for e in S2["entries"] if e["n"] not in gone]
    newn = {e["n"]: i + 1 for i, e in enumerate(keep)}
    for e in keep:
        if e.get("target") is not None:
            if e["target"] not in newn:
                return None
            e["target"] = newn[e["target"]]
        e["n"] = newn[e["n"]]
    S2["entries"] = keep
    return S2


# ------------------------------------------------------------------------------------------------ driver

def worker(args):
    card, purpose, n_rows, probs, seed_tag, parser, sha = args
    global GIT_SHA
    GIT_SHA = sha
    t0 = time.time()
    g = Gen(card, purpose, n_rows, probs, seed_tag, parser=parser).run()
    for r in g.rows:
        r.pop("_info", None)
    return {"card_id": card["card_id"], "rows": g.rows, "rels": g.rels, "side": g.side, "fail": dict(g.fail),
            "skips": dict(g.skips), "alt": dict(g.alt_log), "secs": time.time() - t0, "logs": g.log_no,
            "lenlog": g.lenlog[:400]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=["candidates", "qc", "dev", "test"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cards", default="")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--no-parser", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    sha = git_sha()
    if a.part == "dev":
        cards = CARDS.make_dev_cards()
    else:
        cards = CARDS.make_training_cards()
    import cardfit
    fitrep = cardfit.fit(cards, tokenizer())
    with open(str(TMP / f"cardfit_{a.part}.json"), "w") as f:
        json.dump(fitrep, f, indent=0)
    if a.cards:
        keep = set(a.cards.split(","))
        cards = [c for c in cards if c["card_id"] in keep]
    n_rows = plan_rows(cards, a.part, a.scale)
    probs = qt_probs(cards, n_rows)
    seed_tag = {"candidates": "cand-r1", "qc": "qc-r1", "dev": "dev-r1", "test": "test"}[a.part]
    jobs = [(c, a.part, n_rows[c["card_id"]], probs[c["card_id"]], seed_tag, not a.no_parser, sha) for c in cards]
    out_path = a.out or str(OUT / {"candidates": "candidates_r1.jsonl", "qc": "qc_sample.jsonl",
                                   "dev": "mixdev_S5.jsonl", "test": "test_rows.jsonl"}[a.part])
    log_progress(f"build {a.part}: {len(cards)} cards, target rows {sum(n_rows.values())}, workers {a.workers}")
    res = []
    with mp.get_context("fork").Pool(a.workers) as pool:
        for i, r in enumerate(pool.imap_unordered(worker, jobs)):
            res.append(r)
            if (i + 1) % 10 == 0:
                log_progress(f"build {a.part}: {i + 1}/{len(jobs)} cards done, rows so far "
                             f"{sum(len(x['rows']) for x in res)}")
    res.sort(key=lambda r: r["card_id"])
    write_outputs(res, out_path, a.part)


def plan_rows(cards, part, scale):
    """Rows per card. Candidates: 1.5 x 4,500 = 6,750 (+2% margin). QC: >= 5,000 rows (5,600 drawn). Dev: S5 items
    with surplus (the 400 family items and the 300-item depth sweep are selected from them). Card sizes are fitted so
    that the question-type shares land near the family targets (IPF over card sizes, 25 <= rows <= 128)."""
    if part == "dev":
        return {c["card_id"]: max(1, int((110 if c.get("deep_card") else 70) * scale)) for c in cards}
    elif part == "qc":
        total = int(5600 * scale)
    elif part == "test":
        total = int(40 * len(cards) * scale)
    else:
        total = int(CAND_ROWS * 1.02 * scale)
    probs = qt_probs(cards, {c["card_id"]: 1 for c in cards})
    n = {c["card_id"]: total / len(cards) for c in cards}
    lo, hi = (25 * scale, 124 * scale) if part in ("candidates", "qc") else (1, 10 ** 6)
    for _ in range(200):
        tot = sum(n.values())
        share = collections.Counter()
        for c in cards:
            for q, v in probs[c["card_id"]].items():
                share[q] += n[c["card_id"]] * v / tot
        for c in cards:
            f = sum(v * QT_TARGET[q] / max(1e-6, share[q]) for q, v in probs[c["card_id"]].items())
            n[c["card_id"]] = min(hi, max(lo, n[c["card_id"]] * f))
        z = total / sum(n.values())
        for k in n:
            n[k] = min(hi, max(lo, n[k] * z))
    return {k: max(1, int(round(v))) for k, v in n.items()}


def write_outputs(res, out_path, part):
    rows = [r for x in res for r in x["rows"]]
    side = [s for x in res for s in x["side"]]
    rels = [r for x in res for r in x["rels"]]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    base = out_path[:-6]
    with open(base + ".sidecar.jsonl", "w", encoding="utf-8") as f:
        for s in side:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(base + ".relations.jsonl", "w", encoding="utf-8") as f:
        for r in rels:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    fail = collections.Counter()
    skips = collections.Counter()
    alt = collections.Counter()
    for x in res:
        fail.update(x["fail"])
        skips.update(x["skips"])
        alt.update(x["alt"])
    rep = {"part": part, "rows": len(rows), "relations": len(rels), "cards": len(res),
           "logs": sum(x["logs"] for x in res), "fail": dict(fail), "skips": dict(skips),
           "alt_check": dict(alt.most_common(60)), "secs_max_card": max((x["secs"] for x in res), default=0),
           "short_cards": [x["card_id"] for x in res if len(x["rows"]) == 0],
           "lenlog": {x["card_id"]: x["lenlog"][:30] for x in res}}
    with open(base + ".build_report.json", "w") as f:
        json.dump(rep, f, indent=1)
    log_progress(f"build {part}: wrote {len(rows)} rows, {len(rels)} relations; fail {sum(fail.values())} "
                 f"(by reason in {os.path.basename(base)}.build_report.json)")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("alt_check", "lenlog")}, indent=1)[:3000])


if __name__ == "__main__":
    main()
