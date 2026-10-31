"""F9 build driver (round 1): per-card unit plan -> rows in the 2.4 row format plus Struct side records.
Resumable per card: each card writes out/parts/<mode>/<card_id>.jsonl (+ .side.jsonl, + .done.json) and a rerun skips
finished cards. Modes: cand (round-1 candidate pool, 1.5x), qc (separate G6 QC sample), dev (S5 mix-tuning dev).
Usage: f9build.py <mode> [--cards a,b,...] [--shard k/n]"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(__import__("os").environ.get("F9_OUT") or (HERE.parent / "out"))
PROG = HERE.parents[2] / "c_build" / "progress_phase2.log"

# repair r1 (option buckets): S6 choice rows reach 5-9 options only rarely (component picks need two named errors;
# value / set picks hit the named-error and token limits), so S6 light cards carry more yes/no rows and S1 / S2 light
# cards (record picks with 5-60 options) carry more choice rows; family 45-55% and each sampler 40-60% still hold
YN_SHARE = {"S1": .36, "S2": .35, "S3": .41, "S4": .32, "S6": .44, "S5": .50}  # family 45-55%, each sampler 40-60%
# bins of choice rows (1.8): a choice row prints its card twice, so it fits the 2,000 cap only in the smallest bin; S4
# choice rows also take the compact long bin (<= 4,000). Yes/no rows take the rest of each sampler's planned bin shares.
CHOICE_BINS = {"S1": [1, 0, 0], "S2": [1, 0, 0], "S3": [1, 0, 0], "S4": [.8, 0, .2], "S6": [1, 0, 0]}
# S4 per card: term cards (definition lines, T30) fit bin 0 less often, so more of their choice rows are compact long
# rows; the family long-row cap (1.8: <= 5% of F9 rows) holds with S4 + S6 long rows near 3-4%
S4_CHOICE_BINS = {"term": [.7, 0, .3], "plain": [.85, 0, .15]}


def bin_weights(s, form, card=None):
    from f9samp import BINS
    if s not in CHOICE_BINS:
        return None
    cw = CHOICE_BINS[s]
    if form != "yn":
        if s == "S4" and card is not None:
            return list(S4_CHOICE_BINS["term" if card.get("terms") else "plain"])
        return list(cw)
    c = 1 - YN_SHARE[s]
    w = [max(0.0, (b[2] - c * x) / (1 - c)) for b, x in zip(BINS[s], cw)]
    return [x / sum(w) for x in w]


def long_share(card, yn_t):
    """Planned share of a card's rows drawn in its sampler's long bin (S4 / S6 bin 2; 1.8 long-row cap)."""
    s = card["sampler"]
    if s not in ("S4", "S6"):
        return 0.0
    return yn_t * bin_weights(s, "yn")[2] + (1 - yn_t) * bin_weights(s, "choice", card)[2]
# repair r1 (G10 option buckets 35 / 35 / 15 / 15): value and set picks reach at most 9 options and often fall back to
# 2-4 (named-error and token limits), so the record forms, the only ones with 10-60 options, take a larger share
CHOICE_MIX = {"S1": {"value": .22, "record": .63, "set": .15}, "S2": {"value": .22, "record": .63, "set": .15},
              "S3": {"value": .14, "record": .74, "set": .12}, "S4": {"value": .14, "record": .70, "set": .16},
              "S6": {"value": .30, "record": .50, "set": .20}, "S5": {"value": .50, "record": .50}}
# unit plan, as shares of a card's rows (1.7, 1.5): pairs count both members
UNIT_SHARE = {"bflip": .13, "vflip": .07, "prem": .04, "neg": .07, "cswap": .03, "attack": .10, "short": .10,
              "none": .05}


# repair r1: heavy cards (yes/no only) take fewer rows so the family yes/no share stays 45-55% while light cards carry
# the choice rows the option-bucket quota needs
HEAVY_ROW_W = {"S1": .40, "S2": .35, "S3": .65, "S4": .80, "S6": .50}  # r2c: S6 .60 -> .50  # row weight of a heavy card (row_targets); light 1.0
# repair r1b (G10 swapped 5 +/- 1% of choice rows): a swap card's choice rows use a term frame while its swapped share
# is below this (r1b: 80% of draws gave 7.6%, r1a 50% with fewer swap cards 2.3%)
SWAP_CARD_SHARE = .36  # repair r2: r2b swapped .0406 cand (4-6%); r2k: builds r2c-r2j .040-.053 (mean .047), centred
# repair r1b (G10 yes/no 45-55%): a light card whose choice rows close (no choice row fits the 1.8 cap) stops at this
# share of its target, so its yes/no rows do not replace the sampler's choice rows; the top-up moves the shortfall to
# light cards whose choice rows stay open (S6 light cards with closed choice were 5 of 11, at 96% yes/no)
CLOSED_STOP = .30
CLOSED_STOP_S = {"S6": .15}  # repair r2c: S6 closed light cards (6 of 11 in r2c, 94% yes/no) stop at 15% of target
# repair r2 (G10 S6 yes/no .614 > .60): a light card whose choice frames are all blocked, or whose rows run past this
# yes/no share (its choice draws keep failing: S6 light cards gave 79 / 81 and 47 / 47 yes/no rows in r1c), stops like
# a closed card; the top-up gives no rows to heavy or closed cards of a sampler already at TOPUP_YN_MAX yes/no
LIGHT_YN_MAX = .62
# repair r2 (G10 masked .0998 / .0996 < 10% of choice rows): a masked light card (its choice rows stay full-card) takes
# this row weight, so masked choice rows sit near 12% (r2b at 1.25: .140 / .132, short-card share .099); sampler totals and the 128-row card cap are unchanged
MASKED_LIGHT_W = 1.20
ID_BOUND = 2  # repair r2: per shard, |yes - no| on each visible looked-up-ID feature a unit may not push past
TOPUP_YN_MAX = .50
_QNUM = __import__("re").compile(r"-?\d+(?:[.,]\d+)?")
HEAVY_YN = 1.0  # a heavy card's choice row cannot fit the 2,000-token cap (its card is printed twice)


def yn_target(card):
    """Per-card yes/no share: heavy cards HEAVY_YN; light cards take the rest of their sampler's yes/no plan
    (section 3 form shares; family 45-55%), so the sampler share holds while choice rows sit on short cards."""
    import f9plan
    s = card["sampler"]
    if s == "S5":
        return YN_SHARE[s]
    if not card.get("light"):
        return HEAVY_YN
    p = f9plan.PROFILE[s]
    nl, nh = sum(p["L"]), sum(p["H"])
    y = (YN_SHARE[s] * (nl + nh) - HEAVY_YN * nh) / nl
    return min(.9, max(.1, y))


def log(msg):
    line = f"[F9] {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    prog = PROG if not __import__("os").environ.get("F9_OUT") else HERE.parent / "tmp" / "logs" / "progress_test.log"
    with open(prog, "a") as f:
        f.write(line + "\n")


def row_targets(mode):
    import f9plan
    if mode == "dev":
        cards = f9plan.plan_s5()
        return [(c, 25) for c in cards]
    cards = f9plan.plan_cards()
    out = []
    for s, n in f9plan.CARDS_R1.items():
        cs = [c for c in cards if c[1] == s]
        tot = int(round(f9plan.ROWS_R1[s] * 1.5)) if mode == "cand" else int(round(57 * n))
        # per-card row weights (G0 1.0: median ~45 rows per card, max 128): heavy cards draw yes/no rows only, so
        # samplers whose light cards already sit at the yes/no floor give heavy cards fewer rows (3.x: 40-60% yes/no
        # per sampler); largest-remainder rounding keeps the sampler total exact
        w = [HEAVY_ROW_W.get(s, 1.0) if not c[3].get("light") else (MASKED_LIGHT_W if c[3].get("masked") else 1.0)
             for c in cs]
        q = [tot * x / sum(w) for x in w]
        k = [int(x) for x in q]
        for i in sorted(range(n), key=lambda i: (k[i] - q[i], i))[:tot - sum(k)]:
            k[i] += 1
        out += list(zip(cs, k))
    return out


class CardBuilder:
    """Builds one card's rows as units (singletons, contrast pairs, relation units) toward the unit and form plan."""

    def __init__(self, card, mode, n_target, ctx):
        import f9g3
        from f9emit import Emitter
        self.card, self.mode, self.n = card, mode, n_target
        self.ctx = ctx
        self.rng = random.Random(f"f9-{mode}-{card['card_id']}")
        self.em = Emitter(card, ctx, self.rng, mode, g3=f9g3.check)
        self.rows, self.sides, self.rels = [], [], []
        self.units = 0
        self.kind_rows = {k: 0 for k in list(UNIT_SHARE) + ["single"]}
        self.form_rows = {"yn": 0, "choice": 0}
        self.cform_rows = {"value": 0, "record": 0, "set": 0}
        self.fail = {}
        self.hints = {"yn": {}, "choice": {}}
        self.bfail = {}
        self.deep_n = 0
        self.swap_rows = 0
        self.long_n = 0
        self.frame_ok, self.frame_bad, self.blocked = {}, {}, set()
        self.unit_base = 0
        s = card["sampler"]
        names = [c["name"] for c in self._cols()]
        self.share = dict(UNIT_SHARE)
        light = card.get("light", False)
        self.yn_target = yn_target(card)
        if mode != "dev":
            for f in ("yn", "choice"):
                w = bin_weights(card["sampler"], f, card)
                if w:
                    self.hints[f]["w"] = w
        self.long_cap = max(1, round(1.05 * long_share(card, self.yn_target) * n_target))
        if mode == "dev":
            self.share = {k: 0 for k in UNIT_SHARE}
        else:
            # label-flip contrast pairs and negation units are yes/no: they sit on heavy cards (1.8 profiles);
            # premise-removal pairs are choice rows showing 'cannot be determined': T2 (light) cards, some T5
            t2 = card["sem"]["world"] == "T2"
            t5 = card["sem"].get("missing") == "T5"
            # contrast sets are generated at about 24% of candidate rows (1.7; C2): S6 has no boundary flip (its
            # questions carry no cell-level boundary), so its value flips carry its share
            s6 = s == "S6"
            # build 11: the 1.7 pair cap (pair rows <= 2/k of CBD rows) halves premise-removal pairs, so value and
            # boundary flips carry more of the 20-25% contrast share
            # repair r1b (G10 twins 20-25%: 18.9%): heavy cards are yes/no only, so their flips raise the twin share
            # without raising the yes/no share; S6 and S3 light cards (twins 12% / 17%) take more flips too
            # repair r2 (G10 twins .216 / .201 and short / no card .099 / .099 in build r2b: flips whose twin
            # changes the asked ID's visible features are redrawn, masked cards carry more rows): flips and short
            # units take a larger share
            self.share.update({"bflip": 0 if s6 else ((.23 if s == "S3" else .21) if light else .52),
                               "vflip": (.21 if light else .56) if s6 else (.08 if light else .30),
                               "neg": .05 if light else .26, "prem": .24 if t2 else (.05 if t5 else 0),
                               "cswap": .06 if (light and s in ("S1", "S2", "S3", "S4")) else 0,
                               "short": (.41 if s == "S3" else .33) if light else .34,  # r2f: short / no card .096 (r2d), .123 / .130 (r2e)
                               "none": .16 if light else 0})
            att_ok = s in ("S4", "S6") or "note" in names
            # repair r1: attacked rows were 2.55% of rows (target about 5%, 3-7%)
            self.share["attack"] = (.24 if light else .22) if att_ok else 0
            from f9rows import SHORT_FRAMES
            if not (SHORT_FRAMES & set(card["menu"])) or s == "S4" or card.get("masked"):
                # masked cards: the legend is a full-card feature, so their choice rows stay full (masked 10-15%)
                # S4: a short card states no T28 units and a JSON / YAML key names none (F9-A29 needs the unit in
                # the header), so an S4 row with a unit-bearing amount cannot be short-card or no-card
                self.share["short"] = self.share["none"] = 0

    def _cols(self):
        sc = self.card["schema"]
        out = []
        for k in ("nums", "cats", "dates", "bools", "dim_nums", "dim_cats", "fact_nums", "fact_cats"):
            out += sc.get(k) or []
        if sc.get("text"):
            out.append(sc["text"])
        return out

    # -------------------------------------------------------------------------------------------- ids
    def new_unit(self):
        self.units += 1
        return f"{self.mode}-{self.card['card_id']}-u{self.units + self.unit_base:04d}"

    def ids(self, unit, k, call=None):
        rid = f"f9-{unit}-{k}"
        seed = int.from_bytes(__import__("hashlib").sha256(rid.encode()).digest()[:4], "big")
        return {"id": rid, "group_id": "f9_g_" + unit, "call_id": call or ("f9_c_" + rid), "seed": seed}

    def note(self, why):
        import re as _re
        k = _re.sub(r"\d+", "#", why)[:90]
        self.fail[k] = self.fail.get(k, 0) + 1
        m = _re.match(r"(?:single|attack base|short base|[a-z]+ base) ([A-Z][A-Z0-9_]+):", why)
        if m and "tokens" not in why:
            fr = m.group(1)
            self.frame_bad[fr] = self.frame_bad.get(fr, 0) + 1
            ok_n = self.frame_ok.get(fr, 0)
            if self.frame_bad[fr] >= 12 and ok_n < 0.05 * (ok_n + self.frame_bad[fr]) and fr in self.card["menu"] \
                    and fr not in self.blocked:
                form = self.card["menu"][fr]
                alive = [f for f, v in self.card["menu"].items() if v == form and f not in self.blocked and f != fr]
                if alive or form != "yn":  # a frame that never yields a row on this card stops being drawn
                    # (logged, reported); a choice form whose frames are all blocked is no longer drawn (pick_form)
                    self.blocked.add(fr)
                    self.fail[f"frame blocked {fr}"] = 1

    # -------------------------------------------------------------------------------------------- plan
    def pick_kind(self):
        made = sum(self.kind_rows.values())
        best, bd = "single", -1.0
        for k, sh in self.share.items():
            if sh <= 0:
                continue
            d = sh * self.n - self.kind_rows[k]
            if d > bd and d >= 1:
                best, bd = k, d
        if best != "single" and self.rng.random() < 0.5 and made < self.n * 0.5:
            return "single"
        return best

    def pick_form(self, need=None):
        s = self.card["sampler"]
        if need:
            return need
        tot = sum(self.form_rows.values()) + 1
        if self.form_rows["yn"] / tot < self.yn_target:
            return "yn"
        # only the choice forms this card's menu has (a card without a set frame never draws a set row)
        forms = {v for f, v in self.card["menu"].items() if f not in self.blocked}
        mix = {f: w for f, w in CHOICE_MIX[s].items() if f in forms} or {"yn": 1.0}
        if "yn" in mix:
            return "yn"
        from f9rows import FAMILY_BUCKETS
        over = self.ctx.fam_share("2-4") - FAMILY_BUCKETS["2-4"]
        if over > 0.01 and "record" not in mix and self.form_rows["yn"] / tot < 0.6 and \
                self.rng.random() < min(0.6, 8.0 * over):
            return "yn"  # repair r1: a card whose record frames are absent or blocked yields yes/no rows instead
        if over > 0.01 and "record" in mix:
            # repair r1 (section 5 option buckets): while the family's 2-4 share is over its 35%, the forms capped at
            # 9 options (value, set) are drawn less often than their mix weight
            for f in ("value", "set"):
                if f in mix:
                    mix[f] *= max(0.1, 1.0 - 10.0 * over)
        ctot = sum(self.cform_rows.values()) + 1
        return max(mix, key=lambda f: mix[f] - self.cform_rows[f] / ctot + self.rng.random() * 0.05)

    def pick_frame(self, form, frames=None):
        menu = self.card["menu"]
        # swap-word cards (5 +/- 1% of choice rows are swapped, section 5): about half of their choice rows use a term
        # frame of any choice form (the set form alone gave 2.4%)
        sw_want = self.swap_rows < SWAP_CARD_SHARE * (self.form_rows["choice"] + 1)
        if self.card.get("swap") and form != "yn" and frames is None and sw_want:
            tfa = [f for f, v in menu.items() if v != "yn" and f in ("V_TCOUNT", "SET_TERM") and f not in self.blocked]
            if tfa:
                return self.rng.choice(tfa)
        fr = [f for f, v in menu.items() if v == form and (frames is None or f in frames)]
        fr = [f for f in fr if f not in self.blocked] or (fr if form == "yn" else [])
        if not fr:
            return None
        if form == "yn" and "Y_PRES" in fr and len(fr) > 1 and getattr(self, "cur_unit", "single") != "neg" and \
                self.rng.random() < 0.8:
            # repair r1 (G7 f9:qid_unlisted, 1.9): a presence question on an unlisted id is 'no'; outside a negation
            # unit (whose negated twin on the same id is 'yes') the presence frame is drawn at 1/5 of its weight, for
            # listed and unlisted ids alike, so its question shape stays label-balanced
            fr = [f for f in fr if f != "Y_PRES"]
        tf = [f for f in fr if f in ("V_TCOUNT", "SET_TERM")]
        if self.card.get("swap") and tf and sw_want:
            return self.rng.choice(tf)
        if self.card.get("swap") and form != "yn" and not sw_want and len(tf) < len(fr):
            fr = [f for f in fr if f not in tf]
        if form == "record" and "R_INV" in fr and self.rng.random() < 0.45:
            return "R_INV"
        return self.rng.choice(fr)

    # -------------------------------------------------------------------------------------------- emit / commit
    def emit(self, res, ids, mode="full", rend=None, twin=None):
        from f9samp import Retry
        rend = dict(rend or {})
        from f9ast import depth as _depth
        q = res["q"]
        if _depth(q if q["op"] != "not" else q["inner"], self.card.get("terms") or {}, False) >= 4 and \
                self.deep_n + 1 > 0.08 * self.n:
            raise __import__("f9samp").Retry("deep cap (1.2: deep items <= 10% of rows)")
        if "wid" not in rend:
            rend["wid"] = self.em.pick_wording(res["form"])
        if "style" not in rend:
            rend["style"] = self.em.pick_style()
        if "container" not in rend:
            rend["container"] = self.container(res, exclude_fw=bool(res.get("attacked")))
        try:
            row, side = self.em.finish(res, mode=mode, container=rend["container"], style=rend["style"],
                                       wid=rend["wid"], ids=ids, twin=twin)
        except Exception as e:
            if str(e).startswith("tokens"):
                _shrink(self, res, "yn" if res["form"] == "yn" else "choice")
                if res.get("plan"):
                    key = (res["frame"], res["plan"]["bucket"])
                    self.bfail[key] = self.bfail.get(key, 0) + 1
                    if self.bfail[key] >= 6 and res["plan"]["bucket"] != "2-4":
                        if not hasattr(self.em, "bucket_block"):
                            self.em.bucket_block = {}
                        self.em.bucket_block.setdefault(res["frame"], set()).add(res["plan"]["bucket"])
            raise
        side["unit_kind"] = None
        if row["meta"]["deep"] and self.deep_n + 1 > 0.08 * self.n:
            raise __import__("f9samp").Retry("deep cap (1.2: deep items <= 10% of rows)")
        if res["form"] != "yn" and self.mode != "dev":
            # repair r2 (G6 options / metadata views, G7 choice kinds): a choice row whose gold would push a visible
            # option-kind cell (kind; frame, depth or option count x kind) past its bound is redrawn (f9kinds)
            import f9kinds
            bad = f9kinds.kind_bad(self.ctx.kres, self.ctx.kvar, f9kinds.kind_deltas(row, side, res["frame"]))
            if bad:
                raise __import__("f9samp").Retry("kind balance " + "/".join(bad[0][:-1]) + " " + bad[0][-1])
        return row, side, rend

    def container(self, res, exclude_fw=False):
        card = self.card
        s = card["sampler"]
        if s == "S4" and res["struct"].get("compact"):
            opts = [c for c in card["containers"] if c in ("json_compact", "jsonl")]
            c = self.rng.choice(opts)
            self.em.cont_count[c] = self.em.cont_count.get(c, 0) + 1
            return c
        form = "yn" if res["form"] == "yn" else "choice"
        bi = res["struct"].get("bin", 0) or 0
        if s == "S6" and ((self.hints.get(form) or {}).get(bi) or {}).get("small"):
            # 1.8: the row takes a lighter log syntax from the card's set; the least-used rule in pick_container keeps
            # the card's four syntaxes balanced over all of its rows (3.5)
            syn = min(("isocomp", "syslog"), key=lambda o: self.em.cont_count.get(o, 0) + self.rng.random())
            self.em.cont_count[syn] = self.em.cont_count.get(syn, 0) + 1
            return (syn, "fence" if self.rng.random() < 0.7 else "indent")
        if s != "S6" and ((self.hints.get(form) or {}).get(bi) or {}).get("small"):
            # 1.8 / F9-R1-30: nothing fit inside the bin, so the row takes a lighter container from the card's set
            light = {"S4": ("json_compact", "jsonl")}.get(s, ("csv", "md"))
            opts = [c for c in card["containers"] if c in light and not (exclude_fw and c == "fw")]
            if opts:
                k1 = min(opts, key=lambda o: self.em.cont_count.get(o, 0) + self.rng.random())
                self.em.cont_count[k1] = self.em.cont_count.get(k1, 0) + 1
                self.note(f"light container {form} {k1}")
                if s == "S3":
                    return (k1, k1 if self.rng.random() < 0.6 or len(opts) < 2 else [o for o in opts if o != k1][0])
                return k1
        for _ in range(8):
            c = self.em.pick_container()
            flat = c if isinstance(c, str) else (c[0] if s == "S6" else c)
            if exclude_fw and ("fw" in (flat if isinstance(flat, tuple) else (flat,))):
                continue
            return c
        raise __import__("f9samp").Retry("container")

    def commit(self, items, kind, rels=()):
        """items: [(row, side, res)]; all rows of a unit are written together."""
        for row, side, res in items:
            side["unit_kind"] = kind
            side["struct"] = res["struct"]
            side["gold_payload"] = res["gold"]
            side["options_full"] = [list(o) for o in res.get("options") or []]
            side["shown"] = res.get("shown")
            side["short_text"] = res.get("short_text")
            side["style"] = row["meta"]["format_style"]
            self.rows.append(row)
            self.sides.append(side)
            wid = row["meta"]["wording_id"]
            self.em.word_acc[wid] = self.em.word_acc.get(wid, 0) + 1
            if res["form"] != "yn" and self.mode != "dev":
                import f9kinds
                for c, (d, w) in f9kinds.kind_deltas(row, side, res["frame"]).items():
                    self.ctx.kres[c] = self.ctx.kres.get(c, 0.0) + d
                    self.ctx.kvar[c] = self.ctx.kvar.get(c, 0.0) + w
            self.kind_rows[kind] = self.kind_rows.get(kind, 0) + 1
            self.deep_n += bool(row["meta"]["deep"])
            self.frame_ok[res["frame"]] = self.frame_ok.get(res["frame"], 0) + 1
            hk = self.hints.setdefault("yn" if res["form"] == "yn" else "choice", {}).setdefault(
                res["struct"].get("bin", 0) or 0, {})
            hk["ok"] = hk.get("ok", 0) + 1
            if (side.get("real_tokens") or 0) >= 2000 and (self.card["sampler"], res["struct"].get("bin")) in LONG_BINS:
                self.long_n += 1
                if self.long_n >= self.long_cap:
                    # 1.8: long rows only from the long bins, at their planned share (12% of S4 / S6 rows)
                    for f in ("yn", "choice"):
                        self.hints.setdefault(f, {}).setdefault(2, {})["dead"] = True
            if res["form"] == "yn":
                self.form_rows["yn"] += 1
                self.ctx.take_yes(("w", row["meta"]["wording_id"]), row["gold"])
                self.ctx.take_yes((row["meta"]["wording_id"], side["k_all"]), row["gold"])
                self.ctx.take_yes(("f", side.get("frame")), row["gold"])
                if not _QNUM.search(side.get("qtext") or ""):
                    self.ctx.take_yes(("qn0",), row["gold"])
                import f9kinds
                for f in f9kinds.yn_id_feats(row["state"], side.get("qtext") or ""):
                    self.ctx.take_yes(("id", f), row["gold"])
            else:
                self.form_rows["choice"] += 1
                self.cform_rows[res["form"]] = self.cform_rows.get(res["form"], 0) + 1
                pl = res["plan"]
                if pl:
                    self.ctx.take_bucket(pl["pk"], pl["bucket"])
                    from f9solve_a import CBD, NO_RECORD, NONE, TIE
                    gmap = {"CBD": CBD, "NO_RECORD": NO_RECORD, "NONE": NONE, "TIE": TIE}
                    for a in pl["abst"]:
                        g = res["gold"]
                        isg = (g == gmap[a]) or (a == "NO_RECORD" and isinstance(g, frozenset) and not g)
                        self.ctx.abstain_take(a, pl["k"], isg, res["form"], att=row.get("role") == "attacked")
                if res.get("_rank"):
                    self.ctx.rank_take(*res["_rank"])
                if res.get("_pos"):
                    self.ctx.pos_take(*res["_pos"])
                if side.get("swapped"):
                    self.swap_rows += 1
                if isinstance(side.get("decile"), int):
                    self.ctx.dec[side["decile"]] += 1
                opts = res.get("options") or []
                texts = [o[1] for o in opts]
                gi = texts.index(row["gold"]) if row["gold"] in texts else -1
                if opts:
                    self.ctx.letter_take(len(opts), gi)
                    if gi >= 0:
                        self.ctx.relpos_take(row.get("role") == "attacked", min(3, int(4 * gi / len(opts))))
                if res["form"] == "set" and opts:
                    sets = [o[0] if isinstance(o[0], frozenset) else (frozenset() if o[2] == ["EA", "NO_RECORD"]
                                                                      else None) for o in opts]
                    self.ctx.set_take(len(opts), sets, gi if gi >= 0 else None)
        if kind == "prem" and items and (items[0][2].get("plan") or {}).get("k"):
            self.ctx.pair_take(items[0][2]["plan"]["k"], len(items))
        self.rels += list(rels)

    def cell_ok(self, row, side):
        """G10 negation-count cells (R3-SC2): hold P(yes) per wording x k_all at 50% by accept / reject."""
        if row["qtype"] != "noul":
            return True
        # repair r1b (G6 question view, G7 q_n_numbers = 0): P(yes) is also held per question frame and on questions
        # that print no number (r1b: Y_LEX / Y_EXISTS / Y_TERMX questions without a number were 70% yes)
        cells = [(row["meta"]["wording_id"], side["k_all"]), ("f", side.get("frame"))]
        if not _QNUM.search(side.get("qtext") or ""):
            cells.append(("qn0",))
        # repair r2 (G7 f9:qid_unlisted yes .216): P(yes) is also held on the visible looked-up-ID features (listed /
        # unlisted, above / below every listed ID, first / last ID line), so an unlisted ID does not mean 'no'
        import f9kinds
        if self.mode != "dev":  # S5 dev rows (report-only) keep the r1 cells
            cells += [("id", f) for f in f9kinds.yn_id_feats(row["state"], side.get("qtext") or "")]
        for c in cells:
            y, n = self.ctx.yes.get(c, [0, 0])
            d = y - (n - y)
            if (row["gold"] == 1 and d >= 2) or (row["gold"] == 0 and d <= -2):
                return False
        return True

    def id_ok(self, items):
        """Repair r2 (G7 f9:qid_unlisted: 6 / 43 yes in qc; value flips, negation units and attack pairs on an
        unlisted ID were 'no'): over a unit's yes/no rows, the net yes - no per visible looked-up-ID feature (f9kinds)
        may not push the shard's running count past ID_BOUND (a unit that moves it toward 0 is always kept)."""
        import f9kinds
        if self.mode == "dev":
            return True
        delta = {}
        for row, side, _ in items:
            if row["qtype"] != "noul":
                continue
            for f in f9kinds.yn_id_feats(row["state"], side.get("qtext") or ""):
                delta[f] = delta.get(f, 0) + (1 if row["gold"] == 1 else -1)
        for f, d in delta.items():
            y, n = self.ctx.yes.get(("id", f), [0, 0])
            cur = y - (n - y)
            if abs(cur + d) > ID_BOUND and abs(cur + d) > abs(cur):
                return False
        return True

    # -------------------------------------------------------------------------------------------- base rows
    def hint(self, form):
        self.em.b.size_hint = self.hints["yn" if form == "yn" else "choice"]

    def base_res(self, frame, wid=None, label=None):
        """A base row for a frame. Choice rows draw their display plan first (XF01); a (frame, option bucket) that
        keeps failing on this card (too few eligible ids or the token cap) is blocked, and the realized bucket
        shares are reported."""
        form = self.card["menu"][frame]
        self.hint(form)
        if form == "yn":
            if label is None:
                label = self.ctx.want_yes(self.card, ("w", wid), self.rng)
                fy, fn = self.ctx.yes.get(("f", frame), [0, 0])
                if fy - (fn - fy) >= 1:
                    label = False  # repair r1b: the frame's running yes / no count steers first (cell_ok holds it)
                elif fy - (fn - fy) <= -1:
                    label = True
            return self.em.base(frame, want_label=label)
        plan = self.em.choice_plan(frame)
        try:
            return self.em.base(frame, plan=plan)
        except Exception:
            key = (frame, plan["bucket"])
            self.bfail[key] = self.bfail.get(key, 0) + 1
            if self.bfail[key] >= 6 and plan["bucket"] != "2-4":
                if not hasattr(self.em, "bucket_block"):
                    self.em.bucket_block = {}
                self.em.bucket_block.setdefault(frame, set()).add(plan["bucket"])
                self.note(f"bucket blocked {frame} {plan['bucket']}")
            raise

    def u_single(self):
        from f9samp import Retry
        form = self.pick_form()
        for att in range(6):
            frame = self.pick_frame(form) or self.pick_frame("yn")
            wid = self.em.pick_wording(self.card["menu"][frame])
            try:
                res = self.base_res(frame, wid)
                unit = self.new_unit()
                row, side, _ = self.emit(res, self.ids(unit, "a"), rend={"wid": wid})
            except (Retry, *ERRS) as e:
                self.note(f"single {frame}: {str(e)[:50]}")
                continue
            if not self.cell_ok(row, side):
                self.note("cell balance")
                continue
            if self.card.get("swap") and frame in ("V_TCOUNT", "SET_TERM") and not side.get("swapped") and att < 4:
                self.note("swap word not live")  # the usual reading would not change gold: redraw (section 5)
                continue
            self.commit([(row, side, res)], "single")
            return True
        return False

    def yn_base(self, frames=None, tries=5):
        """A full-card yes/no base row (res, row, side, rend)."""
        from f9samp import Retry
        for att in range(tries):
            frame = self.pick_frame("yn", frames)
            if frame is None:
                return None
            wid = self.em.pick_wording("yn")
            try:
                res = self.base_res(frame, wid)
                return res, wid
            except (Retry, *ERRS) as e:
                self.note(f"yn base {frame}: {str(e)[:50]}")
        return None

    # -------------------------------------------------------------------------------------------- contrast pairs
    def u_flip(self, kind):
        from f9samp import Retry
        from f9units import fact_flip
        for att in range(5):
            b = self.yn_base()
            if not b:
                return False
            res, wid = b
            tw = fact_flip(self.em, res, "boundary" if kind == "bflip" else "value")
            if tw is None:
                self.note(f"{kind}: no flip")
                continue
            unit = self.new_unit()
            try:
                ida = self.ids(unit, "a")
                r1, s1, rend = self.emit(res, ida, rend={"wid": wid})
                r2, s2, _ = self.emit(tw, self.ids(unit, "b"), rend=rend, twin={"of": ida["id"], "kind": "fact_flip"})
            except (Retry, *ERRS) as e:
                self.note(f"{kind} emit: {str(e)[:50]}")
                continue
            import f9kinds
            if f9kinds.yn_id_feats(r1["state"], s1.get("qtext") or "") != \
                    f9kinds.yn_id_feats(r2["state"], s2.get("qtext") or ""):
                # repair r2 (matched twins): the flipped cell may not change the looked-up ID's visible features
                # (r1c: value flips on Y_LEX moved the asked ID off the log, so 'unlisted' meant 'no')
                self.note(f"{kind}: twin changes ID features")
                continue
            if not self.id_ok([(r1, s1, res), (r2, s2, tw)]):
                self.note("id balance")
                continue
            s2["flip"] = tw.get("flip")
            self.commit([(r1, s1, res), (r2, s2, tw)], kind)
            return True
        return False

    def u_prem(self):
        from f9samp import Retry
        from f9units import premise_removal
        card = self.card
        frames = [f for f, v in card["menu"].items() if v != "yn"]
        if card["sem"]["world"] == "T2":
            frames = [f for f in frames if f == "V_LOOK"]
        for att in range(6):
            if not frames:
                return False
            frame = self.rng.choice(frames)
            try:
                plan = self.em.choice_plan(frame)
                if plan["k"] < 3:
                    continue
                if not self.ctx.pair_room(plan["k"]):
                    self.note("prem: pair cap (1.7 / R5-SC1: pair rows <= 2/k of the bucket's CBD rows)")
                    continue
                plan["abst"] = ["CBD"]
                plan["gold_kind"] = "normal"
                self.hint("choice")
                res = self.em.base(frame, plan=plan,
                                   need={"col_type": "cat"} if card["sem"]["world"] == "T2" else None)
            except (Retry, *ERRS) as e:
                self.note(f"prem base {frame}: {str(e)[:50]}")
                continue
            if card["sem"]["world"] == "T2":
                from f9units import _col_of
                loc = _col_of(res["struct"], res["q"].get("col") or "")
                if not loc or loc[2]["type"] != "cat":
                    self.note("prem: T2 lookup column is not a category")  # its value must recur (E0 on the twin)
                    continue
            tw = premise_removal(self.em, res)
            if tw is None:
                self.note("prem: no twin")
                continue
            unit = self.new_unit()
            try:
                ida = self.ids(unit, "a")
                r1, s1, rend = self.emit(res, ida)
                r2, s2, _ = self.emit(tw, self.ids(unit, "b"), rend=rend,
                                      twin={"of": ida["id"], "kind": "premise_removal"})
            except (Retry, *ERRS) as e:
                self.note(f"prem emit: {str(e)[:50]}")
                continue
            self.commit([(r1, s1, res), (r2, s2, tw)], "prem")
            return True
        return False

    # -------------------------------------------------------------------------------------------- relation units
    def u_neg(self):
        from f9samp import Retry
        from f9rows import NEG_FORMS
        from f9units import neg_unit
        dfr = [f for f in NEG_FORMS if f in self.card["menu"]]
        for att in range(5):
            b = self.yn_base(frames=dfr if (dfr and self.rng.random() < 0.65) else None)
            if not b:
                return False
            res, wid = b
            tw = neg_unit(self.em, res, want_dneg=self.rng.random() < 0.85)
            if not tw:
                self.note("neg: no complement")
                continue
            unit = self.new_unit()
            call = "f9_c_" + unit
            try:
                ida = self.ids(unit, "a", call)
                r1, s1, rend = self.emit(res, ida, rend={"wid": wid})
                items = [(r1, s1, res)]
                rels = []
                for k, (tres, tk) in enumerate(tw):
                    try:
                        r2, s2, _ = self.emit(tres, self.ids(unit, "bc"[k], call), rend=rend,
                                              twin={"of": ida["id"], "kind": tk})
                    except (Retry, *ERRS) as e:
                        if tk == "dneg":
                            self.note(f"dneg emit: {str(e)[:50]}")
                            continue
                        raise
                    items.append((r2, s2, tres))
                    rels.append({"a": ida["id"], "b": r2["id"], "type": "complement" if tk == "negation"
                                 else "equiv"})
            except (Retry, *ERRS) as e:
                self.note(f"neg emit: {str(e)[:50]}")
                continue
            if len(items) > 2 and any((sd.get("real_tokens") or 0) >= 2000 for _, sd, _ in items):
                # 1.8: a long row sits in a unit of <= 2 rows, so a long negation unit is emitted without its
                # double-negation twin
                keep_ids = {r["id"] for r, _, _ in items[:2]}
                items = items[:2]
                rels = [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids]
                self.note("long neg unit: dneg twin left out (1.8)")
            if not self.id_ok(items) and len(items) > 2:
                # repair r2: a double-negation twin repeats the base label; on an unlisted ID (base 'no') it is left
                # out when it would unbalance the ID cells
                keep_ids = {r["id"] for r, _, _ in items[:2]}
                items = items[:2]
                rels = [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids]
                self.note("neg unit: dneg twin left out (id balance)")
            if not self.id_ok(items):
                self.note("id balance")
                continue
            self.commit(items, "neg", rels)
            return True
        return False

    def u_cswap(self):
        from f9samp import Retry
        for att in range(5):
            form = self.pick_form()
            frame = self.pick_frame(form) or self.pick_frame("yn")
            wid = self.em.pick_wording(self.card["menu"][frame])
            try:
                res = self.base_res(frame, wid)
                unit = self.new_unit()
                call = "f9_c_" + unit
                ida = self.ids(unit, "a", call)
                r1, s1, rend = self.emit(res, ida, rend={"wid": wid})
                if res["struct"].get("compact"):
                    alt = [c for c in ("json_compact", "jsonl") if c != rend["container"]]
                    c2 = alt[0]
                else:
                    c2 = self.em.pick_container(exclude=rend["container"])
                if c2 == rend["container"]:
                    raise Retry("no other container")
                r2, s2, _ = self.emit(res, self.ids(unit, "b", call), rend=dict(rend, container=c2),
                                      twin={"of": ida["id"], "kind": "container_swap"})
            except (Retry, *ERRS) as e:
                self.note(f"cswap {frame}: {str(e)[:50]}")
                continue
            if r1["gold"] != r2["gold"]:
                self.note("cswap gold differs")
                continue
            if not self.id_ok([(r1, s1, res), (r2, s2, res)]):
                self.note("id balance")
                continue
            self.commit([(r1, s1, res), (r2, s2, res)], "cswap", [{"a": r1["id"], "b": r2["id"], "type": "equiv"}])
            return True
        return False

    def u_attack(self):
        from f9samp import Retry
        from f9units import attack_twin
        for att in range(6):
            form = self.pick_form()
            frame = self.pick_frame(form) or self.pick_frame("yn")
            wid = self.em.pick_wording(self.card["menu"][frame])
            self.em.b.force_note = True  # the attacked free-text cell stays in a lean record (1.8 ladder)
            self.em.att_unit = True  # repair r2: the gold slot follows Ctx.att_slot (G10 attack relpos)
            lab = None
            if self.card["menu"][frame] == "yn":
                # repair r1: attack present stays uncorrelated with the label (G10) at the doubled attack share
                c = self.ctx.yes.get(("attack",), [0, 0])
                lab = (c[0] < c[1] - c[0]) if c[1] else self.rng.random() < 0.5
            try:
                res = self.base_res(frame, wid, label=lab)
            except (Retry, *ERRS) as e:
                self.note(f"attack base {frame}: {str(e)[:50]}")
                continue
            finally:
                self.em.b.force_note = False
                self.em.att_unit = False
            tw = attack_twin(self.em, res)
            if tw is None:
                self.note("attack: no twin")
                continue
            unit = self.new_unit()
            call = "f9_c_" + unit
            try:
                ida = self.ids(unit, "a", call)
                cont = self.container(res, exclude_fw=True)
                r1, s1, rend = self.emit(res, ida, rend={"wid": wid, "container": cont})
                r2, s2, _ = self.emit(tw, self.ids(unit, "b", call), rend=rend,
                                      twin={"of": ida["id"], "kind": "attack"})
            except (Retry, *ERRS) as e:
                self.note(f"attack emit: {str(e)[:50]}")
                continue
            if not self.id_ok([(r1, s1, res), (r2, s2, tw)]):
                self.note("id balance")
                continue
            self.commit([(r1, s1, res), (r2, s2, tw)], "attack", [{"a": r1["id"], "b": r2["id"], "type": "inv"}])
            if res["form"] == "yn":
                self.ctx.take_yes(("attack",), r1["gold"])
            return True
        return False

    # -------------------------------------------------------------------------------------------- short / no card
    def phrases(self, q):
        from f9units import all_atoms
        from f9render import DEFAULT_PH
        out = set()
        if q.get("_ph") and q["op"] == "thr":
            out.add(q["_ph"])
        for a in all_atoms(q):
            a0 = a["arg"] if a["k"] == "not" else a
            if a0["k"] == "cmp" and a0["op"] not in ("=",):
                out.add(a0.get("_ph") or DEFAULT_PH[a0["op"]])
        return sorted(out)

    def short_ok(self, res, mode):
        import copy as _c
        from f9units import all_atoms
        st, q = res["struct"], res["q"]
        for t in st.get("tables") or []:
            if any(v is None for r in t["rows"] for v in r):
                return False
        if any(a.get("k") == "line" and a.get("lvl_op") in (">=", ">", "<=", "<") for a in all_atoms(q)):
            return False
        if any(a.get("k") in ("between", "term") for a in all_atoms(q)):
            return False
        m = self.card.get("masked")
        if m and m["col"] in json.dumps(q, default=str):
            return False
        if res["form"] != "yn" and res["plan"] and res["plan"]["abst"] and mode == "none":
            return False
        return True

    def u_short(self, mode):
        from f9samp import Retry
        from f9cards import clauses, t10_sentences
        from f9rows import SHORT_FRAMES
        card = self.card
        frames = [f for f in card["menu"] if f in SHORT_FRAMES]
        if mode == "none":
            frames = [f for f in frames if card["menu"][f] == "yn" or f in ("V_COUNT", "V_LCOUNT")]
        for att in range(8):
            if not frames:
                return False
            # the card's form plan holds on its short / no-card rows too: a choice frame when yes/no is ahead
            tot = sum(self.form_rows.values()) + 1
            want_ch = self.form_rows["yn"] / tot >= self.yn_target
            pool = [f for f in frames if (card["menu"][f] != "yn") == want_ch and f not in self.blocked] or frames
            frame = self.rng.choice(pool)
            form = card["menu"][frame]
            wid = self.em.pick_wording(form)
            try:
                if form == "yn":
                    res = self.base_res(frame, wid)
                else:
                    plan = self.em.choice_plan(frame)
                    plan["abst"], plan["gold_kind"] = [], "normal"
                    self.hint("choice")
                    res = self.em.base(frame, plan=plan)
            except (Retry, *ERRS) as e:
                self.note(f"{mode} base {frame}: {str(e)[:40]}")
                continue
            if not self.short_ok(res, mode):
                self.note(f"{mode}: not eligible")
                continue
            if mode == "none":
                from f9units import _base
                b = _base(res["q"])
                b["_scope"] = True
            ph = self.phrases(res["q"])
            recs = dict(clauses(card, card["used"]))["Records"]
            t10 = t10_sentences(dict(card, cmp_count=ph, cmp_amount=[])) if ph else []
            res["short_text"] = recs + t10
            res["short_flags"] = ph
            stated = {"T10"} if mode == "short" else set()
            try:
                if not self.em.invariant(res, mode, stated):
                    self.note(f"{mode}: unstated flag live")
                    continue
            except (Retry, *ERRS) as e:
                self.note(f"{mode} invariance: {str(e)[:40]}")
                continue
            res["edge"] = []
            unit = self.new_unit()
            try:
                row, side, _ = self.emit(res, self.ids(unit, "a"), mode=mode, rend={"wid": wid})
            except (Retry, *ERRS) as e:
                self.note(f"{mode} emit: {str(e)[:50]}")
                continue
            if not self.cell_ok(row, side):
                self.note("cell balance")
                continue
            self.commit([(row, side, res)], mode)
            return True
        return False

    # -------------------------------------------------------------------------------------------- run
    def run(self):
        fns = {"single": self.u_single, "bflip": lambda: self.u_flip("bflip"), "vflip": lambda: self.u_flip("vflip"),
               "prem": self.u_prem, "neg": self.u_neg, "cswap": self.u_cswap, "attack": self.u_attack,
               "short": lambda: self.u_short("short"), "none": lambda: self.u_short("none")}
        if self.card["sampler"] in ("S3", "S6"):
            self.share["none"] = 0
        stall = run = 0
        lim = max(60, 4 * self.n)
        n0 = self.n
        # repair r2c (G11 >= 5 wordings per card): a closed / stalled light card that stops early keeps going (up to its
        # first target) until its accepted rows show 5 wordings
        while (len(self.rows) < self.n or (self.n < n0 and len(self.rows) < n0 and
                                           sum(1 for v in self.em.word_acc.values() if v) < 5)) \
                and stall < lim and run < 60:
            hy, hc = self.hints.get("yn") or {}, self.hints.get("choice") or {}
            if self.card["sampler"] in ("S4", "S6"):
                # a form with no fitting draw in bin 0 keeps the long bin (<= 4,000 tokens) up to the 12% long share
                for h in (hy, hc):
                    if (h.get(0) or {}).get("dead") and not (h.get(2) or {}).get("dead"):
                        h[0]["redirect"] = 2
                        h.setdefault(1, {})["redirect"] = 0
            closed = {f: (h.get(0) or {}).get("dead") and (self.card["sampler"] not in ("S4", "S6") or
                                                           (h.get(2) or {}).get("dead")) for f, h in
                      (("yn", hy), ("choice", hc))}
            if closed["choice"] and self.yn_target < 1.0:
                self.yn_target = 1.0  # 1.8: no choice row of this card fits; logged and reported
                self.fail["choice closed (1.8 cap)"] = 1
                if self.card.get("light") and self.mode != "dev":
                    self.n = min(self.n, max(len(self.rows), int(round(CLOSED_STOP_S.get(self.card['sampler'], CLOSED_STOP) * self.n))))
                log(f"{self.mode} {self.card['card_id']} choice rows closed (1.8 cap); card continues yes/no only, stops at {self.n}")
            if self.card.get("light") and self.mode != "dev" and self.yn_target < 1.0:
                open_ch = {v for f, v in self.card["menu"].items() if f not in self.blocked} - {"yn"}
                nr = len(self.rows)
                if not open_ch or (nr >= 20 and self.form_rows["yn"] / nr > LIGHT_YN_MAX):
                    self.yn_target = 1.0
                    self.fail["choice stalled (repair r2)"] = 1
                    self.n = min(self.n, max(nr, int(round(CLOSED_STOP_S.get(self.card['sampler'], CLOSED_STOP) * self.n))))
                    log(f"{self.mode} {self.card['card_id']} choice stalled (yes/no {self.form_rows['yn']}/{nr}); stops at {self.n}")
            if closed["yn"]:
                self.fail["yes/no closed (1.8 cap)"] = 1
                log(f"{self.mode} {self.card['card_id']} yes/no rows closed (1.8 cap); card stops at {len(self.rows)}")
                break
            kind = self.pick_kind() if self.n - len(self.rows) > 2 else "single"
            if kind == "single" and self.n - len(self.rows) > 2 and self.mode != "dev" and \
                    self.kind_rows["single"] >= self.n * 0.45:
                kind = max((k for k in self.share if self.share[k] > 0),
                           key=lambda k: self.share[k] * self.n - self.kind_rows[k], default="single")
            self.cur_unit = kind
            ok = fns[kind]()
            if not ok and kind != "single":
                self.share[kind] *= 0.8 if kind == "attack" else 0.6
                self.note(f"unit {kind} failed; share cut")
                self.cur_unit = "single"
                ok = fns["single"]()
            run = 0 if ok else run + 1
            if not ok:
                stall += 1
        return self.rows


ERRS = ()


def _init_errs():
    global ERRS
    from f9solve_a import Reject, Undefined
    ERRS = (Undefined, Reject, KeyError, ValueError, TypeError, IndexError, ZeroDivisionError, AttributeError)


# ------------------------------------------------------------------------------------------------ side encoding
def enc(x):
    from fractions import Fraction
    if isinstance(x, Fraction):
        return {"$F": f"{x.numerator}/{x.denominator}"}
    if isinstance(x, frozenset):
        return {"$S": sorted(enc(v) for v in x)}
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    if callable(x):
        return None
    return x


def dec(x):
    from fractions import Fraction
    if isinstance(x, dict):
        if "$F" in x and len(x) == 1:
            return Fraction(x["$F"])
        if "$S" in x and len(x) == 1:
            return frozenset(dec(v) for v in x["$S"])
        return {k: dec(v) for k, v in x.items()}
    if isinstance(x, list):
        return [dec(v) for v in x]
    return x


# ------------------------------------------------------------------------------------------------ per card IO
def parts_dir(mode):
    d = OUT / "parts" / mode
    d.mkdir(parents=True, exist_ok=True)
    return d


def build_card(mode, ct, n, ctx, tag=None):
    import f9plan
    cid, s, pack, fl = ct
    d = parts_dir(mode)
    stem = cid if not tag else f"{cid}.{tag}"
    done = d / f"{stem}.done.json"
    if done.exists():
        return json.loads(done.read_text())
    t0 = time.time()
    card = f9plan.finalize(cid, s, pack, fl, held_out=(mode == "dev"))
    cb = CardBuilder(card, mode, n, ctx)
    if tag:  # top-up part (fills a sampler's shortfall on its productive cards): own seed and unit ids
        cb.rng.seed(f"f9-{mode}-{cid}-{tag}")
        cb.unit_base = 10000 * int(tag[1:])
    cb.run()
    with open(d / f"{stem}.jsonl.tmp", "w") as f:
        for r in cb.rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(d / f"{stem}.side.jsonl.tmp", "w") as f:
        for sd in cb.sides:
            f.write(json.dumps(enc(sd), ensure_ascii=False, default=str) + "\n")
    with open(d / f"{stem}.rel.jsonl.tmp", "w") as f:
        for x in cb.rels:
            f.write(json.dumps(x) + "\n")
    for ext in ("jsonl", "side.jsonl", "rel.jsonl"):
        (d / f"{stem}.{ext}.tmp").replace(d / f"{stem}.{ext}")
    info = {"card_id": cid, "tag": tag, "sampler": s, "pack": pack["pack_id"], "target": n, "rows": len(cb.rows),
            "kinds": cb.kind_rows, "forms": cb.form_rows, "cforms": cb.cform_rows, "fail": cb.fail,
            "secs": round(time.time() - t0, 1), "ctx_log": dict(ctx.log)}
    done.write_text(json.dumps(info))
    log(f"{mode} {stem} rows {len(cb.rows)}/{n} in {info['secs']}s")
    return info


def card_parts(d, cid):
    """Finished part stems of a card: the base part, then its top-up parts (t1, t2, ...) in order."""
    out = [cid] if (d / f"{cid}.done.json").exists() else []
    tags = sorted(int(p.name[len(cid) + 2:-len(".done.json")]) for p in d.glob(f"{cid}.t*.done.json"))
    return out + [f"{cid}.t{k}" for k in tags]


def topup_plan(mode, tag):
    """Per sampler, the shortfall against the 1.5x plan (all base parts finished) goes to the sampler's productive
    cards (yield >= 50% of target), in proportion to their yield, capped at 128 rows per card (2.1)."""
    d = parts_dir(mode)
    tg = row_targets(mode)
    got, closed, syn = {}, set(), {}
    for ct, n in tg:
        rows = 0
        for st in card_parts(d, ct[0]):
            if st.endswith(tag):
                continue
            dj = json.loads((d / f"{st}.done.json").read_text())
            rows += dj["rows"]
            fy = syn.setdefault(ct[1], [0, 0])
            fy[0] += (dj.get("forms") or {}).get("yn", 0)
            fy[1] += dj["rows"]
            if "choice closed" in json.dumps(dj.get("fail")) or "choice stalled" in json.dumps(dj.get("fail")):
                closed.add(ct[0])
        got[ct[0]] = rows
    plan = {}
    for s in sorted({ct[1] for ct, _ in tg}):
        cs = [(ct, n) for ct, n in tg if ct[1] == s]
        short = sum(n for _, n in cs) - sum(got[ct[0]] for ct, _ in cs)
        if short <= 0:
            continue
        el = [(ct, n) for ct, n in cs if got[ct[0]] >= 0.5 * n and got[ct[0]] < 128]
        # repair r1b: heavy cards and cards whose choice rows closed draw yes/no only; the shortfall goes to light
        # cards with open choice rows when there are any (G10 yes/no 45-55%, per sampler 40-60%)
        el2 = [(ct, n) for ct, n in el if ct[3].get("light") and ct[0] not in closed]
        if el2:
            el = el2
        elif syn.get(s, [0, 0])[0] >= TOPUP_YN_MAX * max(1, syn.get(s, [0, 1])[1]):
            # repair r2: a sampler already at TOPUP_YN_MAX yes/no keeps its shortfall rather than add yes/no-only rows
            el = []
        w = {ct[0]: got[ct[0]] / n for ct, n in el}
        tw = sum(w.values()) or 1
        for ct, n in sorted(el, key=lambda x: -w[x[0][0]]):
            k = min(128 - got[ct[0]], int(round(short * w[ct[0]] / tw * 1.1)) + 1)
            if k > 0:
                plan[ct[0]] = k
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["cand", "qc", "dev"])
    ap.add_argument("--cards", default=None)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--topup", default=None, help="top-up tag t1, t2, ... (after every base part is finished)")
    a = ap.parse_args()
    _init_errs()
    from f9rows import Ctx
    k, n = (int(x) for x in a.shard.split("/"))
    tg = row_targets(a.mode)
    want = set(a.cards.split(",")) if a.cards else None
    ctx = Ctx()
    ctx.par = 1 if (k + (int(a.topup[1:]) if a.topup else 0)) % 2 == 0 else -1  # repair r2e: min / max side per shard
    scale = float(__import__("os").environ.get("F9_NSCALE") or 1)  # pilot runs only
    tp = topup_plan(a.mode, a.topup) if a.topup else None
    if tp is not None:
        log(f"{a.mode} top-up {a.topup} shard {a.shard}: {sum(tp.values())} rows over {len(tp)} cards")
    for i, (ct, rows) in enumerate(tg):
        if i % n != k or (want and ct[0] not in want):
            continue
        if tp is not None and ct[0] not in tp:
            continue
        try:
            nn = tp[ct[0]] if tp is not None else max(4, int(round(rows * scale)))
            build_card(a.mode, ct, nn, ctx, tag=a.topup)
        except Exception as e:
            log(f"{a.mode} {ct[0]} FAILED {type(e).__name__}: {str(e)[:120]}")
            traceback.print_exc()


LONG_BINS = {("S4", 2), ("S6", 2)}


def tok_cap(s, bi):
    """1.8 caps on the served prompt: 4,000 in the two long bins, else < 2,000."""
    return 4000 if (s, bi) in LONG_BINS else 2000


def _shrink(cb, res, form):
    """1.8 redraw rule after a token overflow, in the spec's order: fewer rows inside the bin (scaled by the measured
    overflow), then fewer columns (down to 4), then the card's lighter containers (F9-R1-30), then the next smaller
    bin (outside the long bins; logged, realized bin shares reported). A (form, bin) where nothing fits is marked
    dead, so its draws stop (logged)."""
    from f9samp import BINS
    st = res["struct"]
    s = cb.card["sampler"]
    bins = BINS.get(s, BINS["S1"])
    bi = st.get("bin", 0) or 0
    tabs = st.get("tables") or []
    t = tabs[1] if (s == "S3" and len(tabs) > 1) else (tabs[0] if tabs else None)
    n = len(t["rows"]) if t else 0
    h = cb.hints.setdefault(form, {})
    hb = h.setdefault(bi, {})
    lo = bins[bi][0]
    tok = getattr(cb.em, "last_tok", None) or 0
    pb = (res.get("plan") or {}).get("bucket")
    cap = 4000 if (pb in ("10-19", "20-60") or (pb == "5-9" and res.get("form") in ("record", "set"))) else \
        tok_cap(s, bi)  # A22: 10+ options; repair r1: record / set picks at 5-9 too
    if n > lo:
        f = min(0.7, cap * 0.95 / tok) if tok else 0.7
        hb["max_rows"] = max(lo, int(n * f))
    elif s in ("S1", "S2", "S4") and not hb.get("max_cols"):
        hb["max_cols"] = 4
    elif s == "S4" and (s, bi) not in LONG_BINS and not hb.get("lean"):
        hb["lean"] = True  # 3.4 floor: id + one scalar + nested object + list field; lists of 0-3 items
        cb.note(f"lean records {s} bin{bi} {form}")
    elif not hb.get("small"):
        hb["small"] = True
        cb.note(f"light containers {s} bin{bi} {form}")
    elif bi > 0 and (s, bi) not in LONG_BINS:
        hb["redirect"] = bi - 1
        cb.note(f"bin down {s} bin{bi} {form}")
        log(f"{cb.mode} {cb.card['card_id']} bin {bi} -> {bi - 1} for {form} rows (token cap)")
    else:
        # bottom of the ladder: draws at the smallest size still fit part of the time (the spec redraws them);
        # close only when they keep failing (>= 20 overflows here and < 10% of this (form, bin)'s draws fit)
        hb["bottom_fail"] = hb.get("bottom_fail", 0) + 1
        if hb["bottom_fail"] < 40 or hb.get("ok", 0) >= 0.05 * (hb.get("ok", 0) + hb["bottom_fail"]):
            return
        hb["dead"] = True
        cb.note(f"bin dead {s} bin{bi} {form}")
        log(f"{cb.mode} {cb.card['card_id']} bin {bi} closed for {form} rows (nothing fits the 1.8 cap)")


if __name__ == "__main__":
    main()
