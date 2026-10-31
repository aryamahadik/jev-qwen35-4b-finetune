"""F10 row samplers for program cards (S1 forward glossary, S2 label-first near misses, S3 code tables, S4 memos).
Display-then-gold (XF01): k and the shown abstain options first, then the gold slot uniformly over the shown slots,
then the case (and on open-world rows the omission set). Every gold is solver A's; rows whose draw breaks a rule are
redrawn and the rejection is counted."""
from __future__ import annotations

from collections import Counter

import model as M
from cases import Cases

BUCKETS = {"2-4": (2, 4), "5-9": (5, 9), "10-19": (10, 19), "20-60": (20, 60)}


class YesCtl:
    """repair r1 (G7): per-card yes-rate controller. The yes/no answer of each ANCHOR follows the card's planned yes
    rate (G0: drawn per card uniformly from 20-80%, applied to anchors as the pre-repair generator did) counted on
    EMITTED anchor yes/no rows (plan["_yn"] = [anchor yes/no rows, anchor yes rows], updated by the emitting loop),
    low-discrepancy with a per-card phase from an RNG of its own. Twins (negation complements, label-flip twins) keep
    their own labels and pull the card toward 50% as designed (matched twins). The old independent draw let a card's
    realised rate drift (a failed draw was redrawn; two candidates cards at 9% / 14% yes made a card-text bigram a
    multi-card G7 cue); counting twins too (build18) spread realised card rates over the full 20-80% and made shared
    card vocabulary a multi-card G7 cue. After two failed draws of one answer in a row the other answer is allowed
    once, so an exhausted answer cannot stall a card."""

    def __init__(self, plan, key):
        import random as _rnd
        plan.setdefault("_yn", [0, 0])
        self.plan = plan
        self.ph = _rnd.Random("ynctl|" + str(key)).random()
        self.fail_run = 0
        self.last = None

    def want(self):
        n, y = self.plan["_yn"]
        w = y < self.plan["yes_rate"] * (n + 1) - self.ph
        if self.fail_run >= 2 and self.last == w:
            w = not w
            self.fail_run = 0
        self.last = w
        return w

    def result(self, ok):
        self.fail_run = 0 if ok else self.fail_run + 1


def note_yn(plan, rows):
    """Feedback for YesCtl: count emitted anchor yes/no rows (qtype noul, not a twin) and their yes golds."""
    yn = plan.setdefault("_yn", [0, 0])
    for x in rows:
        if x.get("qtype") == "noul" and x.get("meta", {}).get("twin_of") is None:
            yn[0] += 1
            yn[1] += int(x["gold"])


def bucket_of(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


class ProgRows:
    def __init__(self, card, r, stats: Counter):
        self.card = card
        self.r = r
        self.cs = Cases(card, r)
        self.stats = stats
        self.ordered = card["ctype"] in ("first", "dlist")
        self.none_ok = card["ctype"] in ("amo", "first", "dlist")
        self.open = card["world"] == "open"
        # repair r1 (G10 open-world omitted shares, G7 n_omitted x abstain cue): per-card share controllers decide
        # whether a determined open-world row omits attributes, and the omitted count (1: 70%, 2: 30%) is drawn the
        # same way for every gold kind (it used to fall back from 2 to 1 or to none depending on the draw)
        self.om = {"ch": [0, 0], "yn1": [0, 0], "yn0": [0, 0]}
        self.ab = {}
        self.ab_fail = 0
        self.om_phase = {}
        self.np_ctr, self.np_phase = [0, 0], r.random()
        self.gcount, self.g_pending = Counter(), None
        self.mix = [0, 0, 0, r.random()]     # emitted rows, choice-type rows (forward choice + inverted), inverted rows, phase

    OM_TARGET = {"ch": 0.62, "yn1": 0.50, "yn0": 0.50}

    def _gold_kind(self, slots):
        """Display-then-gold (XF01) with a stratified gold slot (repair r1, G10 abstain 1/k +/- 2 pp per bucket): per
        option bucket, an abstain slot is gold when the card's running abstain-gold count is >= 0.5 below its
        expectation (sum of n_abstain / k over its emitted choice rows, twins included); otherwise a term slot. The
        abstain option is then uniform over the shown ones, so each is gold at 1/k."""
        ab = [x for x in slots if x != "term"]
        if not ab or self.ab_fail >= 3:     # an abstain gold that keeps failing on this card yields to a term
            return "term"
        e, g = self.ab.setdefault(bucket_of(len(slots)), [self.r.random() - 0.5, 0])
        # the row's own expectation counts with its expected label-flip twins (about 0.12 per choice anchor; a twin
        # never has an abstain gold), so the per-cell deficit stays centred instead of trailing the twins
        if (e + 1.12 * len(ab) / len(slots)) - g >= 0.5:
            return self.r.choice(ab)
        return "term"

    def note_choice(self, spec):
        """Record an emitted choice row (anchor or twin) for the abstain-gold controller."""
        opts = spec.get("options") or []
        ab = [o for o in opts if o in ("none", "cbd")]
        if not ab:
            return
        c = self.ab.setdefault(bucket_of(len(opts)), [self.r.random() - 0.5, 0])
        c[0] += len(ab) / len(opts)
        c[1] += int(spec.get("gold") in ("none", "cbd"))

    def _want_omit(self, key):
        n, m = self.om[key]
        ph = self.om_phase.setdefault(key, self.r.random())     # random phase: no start-up bias per card
        return m < self.OM_TARGET[key] * (n + 1) - ph

    def _count_omit(self, key, omitted):
        self.om[key][0] += 1
        self.om[key][1] += int(bool(omitted))

    def _prior_yes(self, X, case, kind, omitted):
        """Name-prior answer of an affirmative yes/no question on a swapped card (as build_prog.name_prior)."""
        card = self.card
        nat = card.get("natural")
        if not nat or card["mode"] != "swapped" or omitted:
            return None
        met = []
        for t in card["order"]:
            d = nat.get(card["names"][t])
            if d is not None and M.Card({"np": d}, ["np"]).meets("np", case):
                met.append(t)
        if kind == "assigned" and self.ordered:
            return int(bool(met) and met[0] == X)
        return int(X in met)

    def _n_om(self):
        return 1 if self.r.random() < 0.7 else 2

    # ------------------------------------------------------------------------------------------ choice rows
    def choice(self, k, show_none, s3_subset=False):
        """Forward choice row with k options (abstain options count in k)."""
        r, cs, card = self.r, self.cs, self.card
        order = card["order"]
        show_cbd = self.open
        n_abst = int(show_none) + int(show_cbd)
        if k is None:                      # S3 all-codes row: every code shown
            k = len(order) + n_abst
        if self.open and k < 3:
            k = 3
        n_terms = k - n_abst
        if n_terms < 1 or n_terms > len(order):
            return None
        slots = ["term"] * n_terms + (["none"] if show_none else []) + (["cbd"] if show_cbd else [])
        gkind = self._gold_kind(slots)
        # the gold term is drawn once per row, before the case (repair r1, G10 gold card position: redrawing it on
        # every failed case draw favoured terms with large regions, e.g. early decision-list entries)
        # balanced gold terms per card (G10 gold card position): the least-used term is the gold, ties at random;
        # a term whose draw failed is kept for the next call (up to 3 calls), so hard terms are not skipped
        if self.g_pending is not None:
            gterm = self.g_pending[0]
        else:
            m = min(self.gcount[t] for t in order)
            gterm = r.choice([t for t in order if self.gcount[t] == m])
            self.g_pending = None
        for attempt in range(40):
            if gkind == "term":
                gold = gterm
                R = cs.region_for(gold)
            elif gkind == "none":
                gold = "none"
                R = cs.region_for("none")
            else:
                gold = "cbd"
                R = cs.region_for(r.choice(order))
            case = cs.point(R)
            if case is None:
                self.stats["rej_region"] += 1
                continue
            thr = None
            if gkind == "term" and r.random() < 0.25:
                c2, s = cs.move_to_threshold(case, gold, lambda c: cs.answer(c) == {gold})
                if c2 is not None:
                    case, thr = c2, s
            omitted = []
            if self.open and (gkind == "cbd" or self._want_omit("ch")):
                omitted = self._omission(case, gkind == "cbd", self._n_om())
                if omitted is None:
                    self.stats["rej_omit"] += 1
                    continue
            P = cs.answer(case, omitted)
            # shown terms: gold (if a term) + others; XF15: an undetermined P must contain a shown term
            others = [t for t in order if t != gold]
            r.shuffle(others)
            if gkind == "term":
                if P != {gold}:
                    self.stats["rej_gold"] += 1
                    continue
                shown = [gold] + others[:n_terms - 1]
            elif gkind == "none":
                if P != {"none"}:
                    self.stats["rej_gold"] += 1
                    continue
                shown = others[:n_terms] if len(others) >= n_terms else None
                if shown is None:
                    continue
            else:
                if len(P) < 2:
                    self.stats["rej_cbd_determined"] += 1
                    continue
                pt = [t for t in P if t != "none"]
                if not pt:
                    self.stats["rej_xf15"] += 1
                    continue
                must = r.choice(pt)
                rest = [t for t in order if t != must]
                r.shuffle(rest)
                shown = [must] + rest[:n_terms - 1]
            if len(shown) != n_terms:
                continue
            opts = shown + (["none"] if show_none else []) + (["cbd"] if show_cbd else [])
            if gkind == "term" and not show_none and "none" in P:
                continue
            self.ab_fail = 0
            if gkind == "term":
                self.gcount[gold] += 1
                self.g_pending = None
            return {"form": "choice", "case": case, "omitted": sorted(omitted), "options": opts, "gold": gold,
                    "threshold": thr, "P": sorted(P, key=str)}
        self.stats["fail_choice"] += 1
        if gkind != "term":
            self.ab_fail += 1
            self.stats["fail_choice_abstain_gold"] += 1
        else:
            self.g_pending = (gterm, (self.g_pending[1] + 1) if self.g_pending else 1)
            if self.g_pending[1] >= 3:      # a hard term: count the failed tries as a use, so the others go first
                self.gcount[gterm] += 1
                self.g_pending = None
                self.stats["gold_term_hard"] += 1
        return None

    def _omission(self, case, want_undetermined, n):
        """Exactly n omitted attributes: undetermined (CBD) or irrelevant (determined) w.r.t. the full answer; None if
        no such set is found for this case (the caller redraws the case)."""
        cs, r = self.cs, self.r
        slots = list(self.card["legend"])
        if len(slots) < n:
            return None
        base = cs.answer(case)
        # repair r1 (G7, qc_sample): an omission set never hides every digit-bearing attribute (count, qty, amount,
        # date) of a card that has one, for every gold kind alike. Hiding the card's only numeric attribute almost
        # always made the row "cannot be determined", so a record without any number cued the abstain gold (11 of
        # 11 such qc rows; G7 meta state_max_num x option kind)
        digit = [s for s in slots if self.card["legend"][s]["type"] in ("count", "qty", "amount", "date")]
        for _ in range(12):
            om = r.sample(slots, n)
            if digit and all(s in om for s in digit):
                self.stats["omit_keeps_number"] += 1
                continue
            P = cs.answer(case, om)
            if want_undetermined and len(P) >= 2:
                return om
            if not want_undetermined and P == base:
                return om
        return None

    # ------------------------------------------------------------------------------------------ yes/no rows
    def yesno(self, want_yes, kind, s2=False, threshold=False):
        r, cs, card = self.r, self.cs, self.card
        sp = cs.cb.sp
        order = card["order"]
        for attempt in range(40):
            X = r.choice(order)
            R = cs.cb.region(X) if kind == "meets" else cs.cb.assigned_region(X)
            if not want_yes:
                R = sp.comp(R)
                if s2 and kind == "assigned" and self.ordered and r.random() < 0.5:
                    pos = order.index(X)
                    if pos > 0:   # meets X and an earlier-listed term
                        earlier = sp.union(*[cs.cb.region(t) for t in order[:pos]])
                        R = sp.inter(cs.cb.region(X), earlier)
            R = sp.inter(R, [cs.drawbox])
            case = cs.point(R)
            if case is None:
                self.stats["rej_region"] += 1
                continue
            truth = lambda c: (cs.mc.meets(X, c) if kind == "meets" else cs.mc.assigned(X, c, self.ordered))
            if truth(case) != want_yes:
                continue
            thr = None
            if threshold:
                c2, s = cs.move_to_threshold(case, X, lambda c: truth(c) == want_yes)
                if c2 is not None:
                    case, thr = c2, s
            if s2:   # one change away from the opposite truth value (R2-18)
                flip = None
                for s in r.sample(list(cs.leg), len(cs.leg)):
                    for v in cs.one_change(case, s):
                        c2 = dict(case)
                        c2[s] = v
                        if truth(c2) != want_yes:
                            flip = s
                            break
                    if flip is not None:
                        break
                if flip is None:
                    c2, s = cs.move_to_threshold(case, X, lambda c: truth(c) == want_yes)
                    if c2 is None:
                        self.stats["rej_s2_onechange"] += 1
                        continue
                    case, thr = c2, s
                    ok = any(truth({**case, s2_: v}) != want_yes for s2_ in cs.leg for v in cs.one_change(case, s2_))
                    if not ok:
                        self.stats["rej_s2_onechange"] += 1
                        continue
            omitted = []
            key = "yn1" if want_yes else "yn0"
            if self.open and self._want_omit(key):
                slots = list(card["legend"])
                n = self._n_om()
                digit = [s for s in slots if card["legend"][s]["type"] in ("count", "qty", "amount", "date")]
                if len(slots) >= n:
                    for _ in range(12):
                        om = r.sample(slots, n)
                        if digit and all(s in om for s in digit):     # repair r1 (G7): as _omission
                            continue
                        if cs.meets(X, case, om, kind) == {want_yes}:
                            omitted = sorted(om)
                            break
                if not omitted:
                    self.stats["rej_omit_yn"] += 1
                    continue
            pr = self._prior_yes(X, case, kind, omitted)
            if pr is not None and attempt < 30:
                # swapped cards (repair r1, G10 name prior 50 +/- 5 on yes/no rows): stratified case selection keeps
                # "the familiar word's own meaning gives the gold answer" at 50% per card
                n_np, a_np = self.np_ctr
                want_agree = a_np < 0.5 * (n_np + 1) - self.np_phase
                if (pr == int(want_yes)) != want_agree:
                    self.stats["np_strat_redraw"] += 1
                    continue
            if pr is not None:
                self.np_ctr[0] += 1
                self.np_ctr[1] += int(pr == int(want_yes))
            return {"form": "yn", "case": case, "omitted": omitted, "ask": X, "wkind": kind,
                    "gold": 1 if want_yes else 0, "threshold": thr}
        self.stats["fail_yn"] += 1
        return None

    # ------------------------------------------------------------------------------------------ inverted rows
    def inverted(self, k):
        """Exactly one shown record meets X (closed world, at-most-one / partition cards; ST42)."""
        r, cs, card = self.r, self.cs, self.card
        sp = cs.cb.sp
        for attempt in range(30):
            X = r.choice(card["order"])
            good = cs.point(sp.inter(cs.cb.region(X), [cs.drawbox]))
            if good is None:
                continue
            notX = sp.inter(sp.comp(cs.cb.region(X)), [cs.drawbox])
            bad = []
            for _ in range(k * 4):
                c = cs.point(notX)
                if c is not None and c not in bad and c != good:
                    bad.append(c)
                if len(bad) == k - 1:
                    break
            if len(bad) < k - 1:
                continue
            recs = bad + [good]
            r.shuffle(recs)
            return {"form": "inv", "records": recs, "ask": X, "gold_idx": recs.index(good), "k": k}
        self.stats["fail_inv"] += 1
        return None

    # ------------------------------------------------------------------------------------------ S2 distractors
    def s2_options(self, row):
        """S2: every shown non-gold term is a case near miss (one attribute value away from being assigned) or a
        name-error distractor (E1 name prior on swapped cards, E7 look-alike)."""
        cs, card = self.cs, self.card
        n_terms = sum(1 for o in row["options"] if o not in ("none", "cbd"))
        gold = row["gold"]
        case = row["case"]
        ecodes = {}
        cand = []
        for t in card["order"]:
            if t == gold:
                continue
            s = cs.near_miss_any(case, t)
            if s is not None:
                cand.append(t)
                at_slots = {at["a"] for at in M.walk_atoms(card["defs"][t])}
                d = card["defs"][t]
                exc_slots = {at["a"] for at in M.walk_atoms(d.get("exc"))} if d.get("exc") else set()
                oi_slots = {at["a"] for at in M.walk_atoms(d.get("onlyif"))} if d.get("onlyif") else set()
                ty = card["legend"][s]["type"] if not isinstance(s, tuple) else "date"
                ecodes[t] = ("E2" if s in exc_slots else "E4" if s in oi_slots else
                             "E3" if ty in ("count", "qty", "amount", "date") else "E9")
            elif card["mode"] == "swapped" and card.get("natural"):
                nat = card["natural"].get(card["names"][t])
                if nat is not None and M.Card({"np": nat}, ["np"]).meets("np", case):
                    cand.append(t)
                    ecodes[t] = "E1"
            elif card.get("lookalike") and card["names"][t] in card["lookalike"] and \
                    (gold not in ("none", "cbd") and card["names"][gold] in card["lookalike"]):
                cand.append(t)
                ecodes[t] = "E7"
        need = n_terms - (1 if gold not in ("none", "cbd") else 0)
        if gold == "cbd":
            P = [t for t in row["P"] if t != "none"]
            keep = [t for t in row["options"] if t in P][:1]
            cand = [t for t in cand if t not in keep]
            if len(cand) < need - len(keep):
                return None
            self.r.shuffle(cand)
            shown = keep + cand[:need - len(keep)]
        else:
            if len(cand) < need:
                return None
            self.r.shuffle(cand)
            shown = ([gold] if gold != "none" else []) + cand[:need]
        abst = [o for o in row["options"] if o in ("none", "cbd")]
        row["options"] = shown + abst
        row["ecodes"] = {t: ecodes.get(t, "E0") for t in shown if t != gold}
        return row

    # ------------------------------------------------------------------------------------------ groups
    def groups(self, plan):
        """Yield groups (lists of row specs: anchor first) until plan['n_rows'] rows exist."""
        import twins as TW
        r, card = self.r, self.card
        s = card["sampler"]
        n_target = plan["n_rows"]
        yes_rate = plan["yes_rate"]
        made = 0
        gi = 0
        fails = 0
        yctl = YesCtl(plan, card.get("card_id"))
        while plan.get("_emitted", made) < n_target and fails < 60 and gi < 6 * n_target:
            gi += 1
            u = r.random()
            row = None
            # repair r1 (G10 name modes are shares of choice ROWS): a per-card controller keeps choice-type rows
            # (forward choice + inverted, twins included) at plan["choice_rows"] of the card's emitted rows and
            # inverted rows at 30% on inverted cards (AR30), so every card's choice-row count follows its plan
            nrow, nch, ninv, ph = self.mix
            want_ch = nch < plan.get("choice_rows", plan.get("choice_share", 0.5)) * (nrow + 1) - ph
            want_inv = bool(card.get("inverted")) and ninv < 0.30 * (nrow + 1) - ph
            u = 0.0 if want_inv else (0.5 if want_ch else 0.99)
            if fails >= 5 and fails % 2:     # a card whose choice draws keep failing still makes progress
                u = 0.99
            if card.get("inverted") and u < 0.30:
                k = r.randint(5, 9) if s == "S3" else (r.randint(2, 4) if r.random() < 0.55 else r.randint(5, 9))
                k = min(k, plan["inv_kmax"])
                row = self.inverted(k) if k >= 2 else None
            elif u < 0.9:
                k, subset = plan["draw_k"]()
                b0 = bucket_of(k) if k is not None else None
                for _try in range(12):
                    # a failed draw is retried in its own option bucket (repair r1: rejections used to push S2 and S4
                    # rows into the 2-4 bucket and yes/no rows; G10 option buckets)
                    show_none = self.none_ok and (k is None or k >= 3) and r.random() < 0.15
                    row = self.choice(k, show_none)
                    if row is not None and s == "S2":
                        g0 = row["gold"]
                        row = self.s2_options(row)
                        if row is None and g0 in ("none", "cbd"):
                            self.ab_fail += 1
                    if row is not None:
                        break
                    self.stats["choice_retry_same_bucket"] += 1
                    if k is not None and not subset:
                        k = plan["draw_k"].k_in(b0)
                if row is not None and s == "S3" and subset:
                    row["s3_subset"] = True
            else:
                kind = "meets" if r.random() < 0.5 else "assigned"
                r.random()     # the old independent yes draw (keeps the stream); YesCtl decides (repair r1, G7)
                row = self.yesno(yctl.want(), kind, s2=(s == "S2"),
                                 threshold=(r.random() < (0.30 if s == "S2" else 0.25)))
                yctl.result(row is not None)
            if row is None:
                fails += 1
                continue
            fails = 0
            row["gid"] = gi
            group = [row]
            # label-flip twin (about 18% of anchors; R2-13)
            if r.random() < plan["twin_p"]:
                order = ["defswap", "boundary", "exception"]
                w = [0.45, 0.35, 0.20]
                first = r.choices(order, w)[0]
                for kind in [first] + [x for x in order if x != first]:
                    tw = (TW.twin_defswap(card, row, r) if kind == "defswap" else
                          TW.twin_boundary(card, row, r, self.cs) if kind == "boundary" else
                          TW.twin_exception(card, row, r, self.cs))
                    if tw is not None:
                        tw["twin_of"] = "anchor"
                        group.append(tw)
                        self.stats["twin_" + kind] += 1
                        break
            # relation unit (one per group)
            if row["form"] == "yn":
                v = r.random()
                if v < plan["neg_p"] + plan["dneg_p"]:
                    nf = r.randrange(2)
                    group.append({**row, "neg": 1, "neg_form": nf, "gold": 1 - row["gold"], "rel": "complement",
                                  "twin_kind": "neg", "twin_of": "anchor"})
                    if v < plan["dneg_p"]:
                        group.append({**row, "neg": 2, "gold": row["gold"], "rel": "equiv", "twin_kind": "dneg",
                                      "twin_of": "anchor"})
                elif card["mode"] == "invented" and v < plan["neg_p"] + plan["dneg_p"] + plan["nameinv_p"]:
                    group.append({**row, "nameinv": True, "rel": "equiv", "twin_kind": "nameinv", "twin_of": "anchor"})
                elif s in ("S1", "S2", "S3", "S4") and r.random() < plan.get("attack_p_yn", 0.30):
                    group.append({**row, "attack": True, "rel": "inv", "twin_kind": "attack", "twin_of": "anchor"})
            # repair r1 (G7): attack units sit on yes/no rows only. G0 (A18, section 7) has the in-record label agree
            # with gold on 50% of the rows that carry one; on a choice row that names gold at 50% against p0 = 1/k, a
            # cue G7 rejects, while on yes/no rows 50% is p0. G0 asks for program forward rows, not for choice rows.
            for sp in group:
                if sp.get("form") == "choice" and not plan.get("_fb"):     # with _fb the emitting loop counts
                    self.note_choice(sp)
                if self.open and sp.get("form") in ("choice", "yn"):     # omission controllers count emitted rows
                    self._count_omit("ch" if sp["form"] == "choice" else ("yn1" if sp["gold"] == 1 else "yn0"),
                                     sp.get("omitted"))
            self.mix[0] += len(group)
            self.mix[1] += sum(1 for sp in group if sp.get("form") in ("choice", "inv"))
            self.mix[2] += sum(1 for sp in group if sp.get("form") == "inv")
            if row["form"] == "choice":
                plan["draw_k"].note(k if s == "S3" else len(row["options"]), bool(row.get("s3_subset")))
            made += len(group)
            yield group
