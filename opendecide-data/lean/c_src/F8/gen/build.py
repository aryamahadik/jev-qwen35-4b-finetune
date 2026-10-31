"""F8 build pipeline: cards -> units -> structures -> checked rows (candidates, QC sample, S5 mix-tuning dev).

Every emitted row has passed, before it is written: solver A (determined label; abstain only where the plan put it),
the CI lint (every flipping SEM line rendered in the row's card version), the named-error distractor rule (choice rows),
fmt1 loader_check (decoder_io cygnet + schema_branch_mark, random option order, gold letter maps back, check_rows),
the text lints, the real-tokenizer length (< 2,000 counted tokens; instructions appear twice in the served prompt), and
the G3 round trip (independent parser -> same render hash; solver B on the parsed structure -> same label).
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import sys
import time
from fractions import Fraction as Fr

import cardbuild
import cards as CP
import common as CM
import errors as ER
import hashes as H
import lexicon as L
import lints
import packs_f8
import parse as PZ
import plans
import render as RD
import samplers as SP
import semsets as SS
import solver_a as SA
import solver_b as SB
import twins as TW
from fmt1 import card as fcard
from fmt1 import pool as fpool
from fmt1.render import FormatError

GUARD_MULT = 40         # repair r2: unit tries per target row before a card gives up (was 6)
LONG_CAP = 2000          # F8 plans no long rows (G0 1 choice-row layout): counted length < 2,000
HARD_CAP = 7900


# ------------------------------------------------------------------------------------------------ shared tools
class Tools:
    def __init__(self):
        from transformers import AutoTokenizer
        import negcount
        self.tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
        self.dio = fcard._dio()
        self.td = fcard._td()
        self.neg = negcount
        self.wmap = {w["id"]: w for w in CP.wordings()}

    def user_msg(self, raw: dict, perm: list) -> str:
        """decoder_io.user_msg in the served layout; more than 26 options use two-letter labels, as fmt1's loader
        check does (a Readout fills the tokenizer's one-token two-letter set)."""
        import string
        dio = self.dio
        saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
        try:
            dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
            if len(perm) > len(dio.WIDE):
                U = string.ascii_uppercase
                dio.WIDE = list(U) + [a + b for a in U for b in U]
            return dio.user_msg(raw, perm)
        finally:
            dio.STYLE, dio.LAYOUT, dio.WIDE = saved

    def tokens_exact(self, raw: dict, perm: list) -> int:
        """Real-tokenizer length of the served prompt (Qwen3.5 chat template, cygnet system + user message)."""
        s = self.dio.render_chat(self.tok, self.dio.CYGNET_SYSTEM, self.user_msg(raw, perm))
        return len(self.tok(s, add_special_tokens=False)["input_ids"])

    def tokens(self, raw: dict, perm: list) -> int:
        """Fast count used while generating: user-message tokens + the fixed template overhead (+2 margin)."""
        if not hasattr(self, "_overhead"):
            u = "x"
            s = self.dio.render_chat(self.tok, self.dio.CYGNET_SYSTEM, u)
            self._overhead = len(self.tok(s, add_special_tokens=False)["input_ids"]) - \
                len(self.tok(u, add_special_tokens=False)["input_ids"])
        u = self.user_msg(raw, perm)
        return len(self.tok(u, add_special_tokens=False)["input_ids"]) + self._overhead + 2


# ------------------------------------------------------------------------------------------------ depth (G0 1)
def _q_depth(S: dict, e: dict, q: dict) -> int:
    k = q.get("k")
    if k == "risk":
        k = q["def"]
    if k == "score":
        ln = [l for l in S["rules"]["scorecard"]["lines"] if SA.line_points(l, e, S, SA.CV()) != 0]
        return max(0, len(ln) - 1)
    if k == "post":
        b = e["bay"]
        kk = len(b["hyps"])
        if b["form"] in ("counts", "joint"):
            return kk
        if b["form"] == "nE":
            return 1
        d = 2 * kk + kk * (len(b["signs"]) - 1)
        d += kk * sum(1 for s in b["signs"] if not b["sig"][s])
        return d
    if k in ("el", "ev"):
        if e.get("outs"):
            return 2 * len(e["outs"]) - 1
        return 1 if (e.get("ch") or {}).get("amt") is not None else 0
    if k == "tec":
        return 2 * len(e.get("outs") or [])
    if k == "en":
        return 1
    return 0


def depth(S: dict) -> int:
    """Depth from the numbers as rendered; with unknowns, the largest depth over the allowed corner values."""
    slots = SA.unknown_slots(S)
    if slots:
        import itertools
        best = 0
        for combo in itertools.product(*[d for _, d in slots]):
            T = SA.assign(S, slots, combo)
            try:
                best = max(best, _depth_closed(T))
            except (SA.Undetermined, ZeroDivisionError):
                continue
        return best
    return _depth_closed(S)


def _depth_closed(S: dict) -> int:
    f = S["form"]
    ents = S["ents"]
    if f in ("yn_thr", "bin"):
        return _q_depth(S, ents[S["case"]], S["q"])
    if f == "yn_act":
        c = S["rules"]["arules"][S["act"]["action"]]
        ds = [_q_depth(S, ents[S["case"]], p["q"]) for p in c["parts"] if p["t"] == "q"]
        return max(ds or [0])
    if f == "tier":
        return _q_depth(S, ents[S["case"]], {"k": "score"})
    if f == "mat":
        return 1 if S["rules"]["mat"]["impact"] == "expected" else 0
    if f == "pred":
        b = ents[S["case"]]["bay"]
        return len(b["signs"]) if b["form"] == "rates" else 0
    if f == "inv":
        r = S["rules"]["inv"]
        if r["kind"] == "q":
            return max(_q_depth(S, e, r["q"]) for e in ents)
        c = S["rules"]["arules"][r["action"]]
        return max([_q_depth(S, e, p["q"]) for e in ents for p in c["parts"] if p["t"] == "q"] or [0])
    return max(_q_depth(S, e, S["q"]) for e in ents)


def no_float(o) -> bool:
    if isinstance(o, float):
        return False
    if isinstance(o, dict):
        return all(no_float(v) for v in o.values())
    if isinstance(o, (list, tuple)):
        return all(no_float(v) for v in o)
    return True


# ------------------------------------------------------------------------------------------------ the builder
class Builder:
    def __init__(self, tools: Tools, mode: str, seed_tag: str):
        self.T = tools
        self.mode = mode
        self.tag = seed_tag
        self.packs = packs_f8.by_id()
        self.stats = collections.Counter()
        self.parse_fail = collections.Counter()
        self.rows, self.side, self.rels = [], [], []
        self.hashes_seen = set()
        self.mr_on = False
        self.mr = collections.Counter()
        self.mr_fail = []

    # -------------------------------------------------------------------------------------------- one structure
    def check_and_render(self, card: dict, S: dict, info: dict, plan: dict, rng, *, row_id: str,
                         wording_id=None, style_pref=None, inert=None, allow_dup: bool = False):
        """Run every row check; return (row, sidecar, extras) or None (the caller redraws)."""
        st = self.stats
        if not no_float(S):
            st["rej:float"] += 1
            return None
        try:
            sol = SA.solve(S)
        except (SA.Undetermined, ValueError, ZeroDivisionError) as e:
            st["rej:solveA"] += 1
            return None
        f = S["form"]
        yn = f in ("yn_thr", "yn_act")
        if yn and not sol["det"]:
            st["rej:yn_undetermined"] += 1
            return None
        if not yn and S["world"] == "closed" and not sol["det"]:
            st["rej:closed_undetermined"] += 1
            return None
        if f == "inv" and isinstance(sol["ans"], tuple):
            st["rej:inv_shape"] += 1
            return None
        if card.get("_example_ids") and {e["id"] for e in S["ents"]} & card["_example_ids"]:
            st["rej:example_id"] += 1
            return None
        ph = H.problem_hash(S)
        if card.get("_example_hashes") and ph in card["_example_hashes"]:
            st["rej:example_hash"] += 1
            return None
        if ph in self.hashes_seen and not allow_dup:
            st["rej:dup_structure"] += 1
            return None
        dep = depth(S)
        if dep > 6:
            st["rej:depth>6"] += 1
            return None
        version = plan["version"]
        sems = SS.sem_set(card, version)
        base = (repr(sol["ans"]), sol["det"])
        edges, missing = SS.ci_edges(S, sems, base)
        if missing:
            st["rej:ci_missing:" + ",".join(missing)] += 1
            return None
        # options and gold
        dmap = {}
        if yn:
            gold = 1 if sol["ans"] else 0
            opts = None
            gold_text = "Yes" if gold == 1 else "No"
        else:
            canon = RD.options_for(card, S)
            keys = {k: t for t, k in canon}
            gk = RD.gold_key(S, sol["ans"]) if f == "rank_order" else sol["ans"]
            if gk not in keys:
                st["rej:gold_not_shown"] += 1
                return None
            gold_text = keys[gk]
            kof = (lambda a: RD.gold_key(S, a) if isinstance(a, tuple) else a) if f == "rank_order" else (lambda a: a)
            dm = ER.distractor_map(S, gk, kof)
            if S["world"] == "open":
                # on open rows the abstain option and the filled answers are the misreadings SEM-02 names:
                # (b) abstain whenever a fact is not recorded; (a) 'not recorded' read as absent or zero
                for tag, cv in (("SEM-02b", SA.CV(abstain_any=True)), ("SEM-02a", SA.CV(nr_zero=True))):
                    try:
                        a2 = SA.solve(S, cv)["ans"]
                    except (SA.Undetermined, ValueError, ZeroDivisionError):
                        continue
                    if f == "inv" and a2 == "NOTA":
                        a2 = "CBD"
                    if a2 != gk and a2 in keys:
                        dm.setdefault(a2, []).append(tag)
            dmap = {keys[k]: v for k, v in dm.items() if k in keys}
            if not dmap:
                st["rej:no_named_error"] += 1
                return None
            opts = [t for t, _ in canon]
            rng.shuffle(opts)
            gold = gold_text
            if not (2 <= len(opts) <= 60):
                st["rej:n_options"] += 1
                return None
        # wording
        qtype = "noul" if yn else "choice"
        wl = [w for w in card["wordings"] if CP.wording_ok(self.T.wmap[w], qtype,
                                                          {"points", "chance"})]
        if wording_id is None:
            # repair r1 (G11): a per-card cycle over the card's wordings, so every card uses all of its >= 5 wordings
            wkey = "_wcyc_" + qtype
            if wkey not in card:
                card[wkey] = plans.Cycle(CM.rng_for("wcycle", card["card_id"], qtype), wl or card["wordings"])
            wid = card[wkey].next()
        else:
            wid = wording_id
        wtext = self.T.wmap[wid]["text"]
        people = self.packs[card["pack"]]["people"]
        row = {"version": version, "wording": wtext, "qvar": rng.randrange(2), "qt": info.get("qt"),
               "options": opts, "people": people, "inert": inert, "inert_pos": rng.randrange(1000),
               "examples": card.get("_examples") if version == "full" else None}
        styles = list(card["styles"])
        rng.shuffle(styles)
        if style_pref:
            styles = [style_pref] + [s for s in styles if s != style_pref]
        for sid in styles:
            row["style"] = sid
            try:
                fld = RD.render_fields(card, S, row)
            except FormatError:
                continue
            raw = {"id": row_id, "qtype": fld["qtype"], "state": fld["state"], "instructions": fld["instructions"],
                   "card": fld["card"], "options": fld["options"], "gold": gold,
                   "meta": {"format_style": sid}}
            sem_texts = {}
            for k in sems:
                sem_texts.setdefault(SS.base_id(k), []).append(RD.sem_text(card, k))
            probs = lints.lint_row({**raw, "_q": fld["_q"]}, sem_texts)
            if probs:
                st["rej:lint:" + probs[0][:40]] += 1
                return None
            ms = fcard.must_show(fld["_ir"], question=fld["_q"], wording=wtext)
            if version == "none":
                ms = [m for m in ms]
            res = fcard.loader_check(raw, must_show=ms, seed="f8-g15")
            if not res["ok"]:
                st["rej:loader:" + res["problems"][0][:40]] += 1
                return None
            ntok = self.T.tokens(raw, res["perm"])
            if ntok >= LONG_CAP:
                st["rej:long_row"] += 1
                return None
            # G3 round trip
            try:
                P = PZ.parse_row(raw)
                S2 = PZ.assemble(P, raw)
            except Exception as e:     # noqa: BLE001 - any parse failure is a bug to count, then try a new style
                self.parse_fail[f"{f}:{type(e).__name__}:{str(e)[:50]}"] += 1
                continue
            v1, v2 = H.render_view(S), H.render_view(S2)
            if v1 != v2:
                import re as _re
                d = H.first_diff(v1, v2) or ""
                self.parse_fail[f"{f}:view_mismatch:{_re.sub(r'[0-9]', '#', d)[:110]}"] += 1
                continue
            try:
                rb = SB.solve(S2)
            except Exception as e:     # noqa: BLE001
                self.parse_fail[f"{f}:solverB:{type(e).__name__}"] += 1
                continue
            aa = RD.gold_key(S, sol["ans"]) if (f == "rank_order" and isinstance(sol["ans"], tuple)) else sol["ans"]
            if rb["ans"] != aa or rb["det"] != sol["det"]:
                self.parse_fail[f"{f}:solverB_disagree"] += 1
                continue
            okeys = PZ.option_keys(S2, raw)
            pg = okeys.get(raw["gold"] if not yn else ("Yes" if gold == 1 else "No"))
            want = (gold == 1) if yn else (RD.gold_key(S2, rb["ans"]) if f == "rank_order" and isinstance(rb["ans"], tuple) else rb["ans"])
            if pg != want:
                self.parse_fail[f"{f}:gold_option_map"] += 1
                continue
            found = {SS.base_id(k) for k in P["C"]["sems"]}
            need = {SS.base_id(k) for k in sems}
            if not need <= found:
                self.parse_fail[f"{f}:sem_not_found:{sorted(need - found)[:2]}"] += 1
                continue
            gp = None
            if f == "pred":
                gpb = rb.get("gold_probs")
                gpa = sol["post"]
                if gpb != gpa:
                    self.parse_fail["pred:gold_probs_mismatch"] += 1
                    continue
                gp = {raw["options"][i]: None for i in range(len(raw["options"]))}
                for t, kk in RD.options_for(card, S):
                    gp[t] = gpa[kk]
            break
        else:
            st["rej:no_style"] += 1
            return None
        S["_version"], S["_qt"] = version, info.get("qt")
        if not row_id.startswith("example-"):
            self.hashes_seen.add(ph)
        if self.mr_on:
            import mr as MR
            res_mr = MR.run_all(card, S, raw, fld, self, CM.h64("mr", row_id))
            for k_, v_ in res_mr.items():
                if k_.endswith(":exc"):
                    self.mr["exc:" + k_ + ":" + v_[:40]] += 1
                    continue
                self.mr[(k_, f, v_)] += 1
                if not v_ and len(self.mr_fail) < 50:
                    self.mr_fail.append((k_, row_id))
        extras = {"sol": sol, "edges": edges, "depth": dep, "dmap": dmap, "sems": sems, "ntok": ntok,
                  "S2_hash": H.render_hash(S2), "gold_probs": gp, "perm": res["perm"]}
        return raw, fld, extras

    # -------------------------------------------------------------------------------------------- one row record
    def record(self, card, S, info, plan, raw, fld, ex, *, row_id, call_id, twin_of=None, twin_kind=None,
               seed=None, unit_id=None, wording_id=None):
        f = S["form"]
        yn = f in ("yn_thr", "yn_act")
        q = fld["_q"]
        nc = self.T.neg.count(q)
        k_syn, k_all = nc.k_syn, nc.k_all
        meta = {"family": "F8", "spec_id": CM.SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack"],
                "sampler": card["sampler"], "gen_version": CM.GEN_VERSION, "git_sha": GIT_SHA, "seed": seed,
                "structure_hash": H.problem_hash(S), "difficulty_bin": None, "crowd_pg": None,
                "depth": ex["depth"], "deep": ex["depth"] >= 4, "format_style": raw["meta"]["format_style"],
                "wording_id": wording_id, "defs_style": card["defs_style"] if plan["version"] == "full" else
                ("short" if plan["version"] == "short" else "none"),
                "twin_of": twin_of, "twin_kind": twin_kind, "text_source": None, "licence": CM.LICENCE,
                "edge": [f"F8/{e}" for e in ex["edges"]] + (["masked"] if card["label_form"] == "masked" and not yn
                                                            else []) + (["swapped"] if card["label_form"] == "swapped"
                                                                        and not yn else []),
                "subtype": card["sub"], "persona_seed": card.get("persona_seed")}
        if ex["gold_probs"]:
            meta["gold_probs"] = {k: (v.numerator / v.denominator) for k, v in ex["gold_probs"].items()}
        row = {"id": row_id, "group_id": f"c_f8:{card['card_id']}:{unit_id}", "call_id": call_id,
               "source": CM.SOURCE, "state": raw["state"], "qtype": raw["qtype"], "instructions": raw["instructions"],
               "options": raw["options"], "gold": raw["gold"], "role": None, "card": raw["card"], "meta": meta}
        side = {"id": row_id, "card_id": card["card_id"],
                "qform": {"yn_thr": "YN", "yn_act": "YN", "bin": "BIN", "tier": "TIER", "mat": "MAT",
                          "rank_top": "RANK-top", "rank_order": "RANK-order", "dec": "DEC", "pred": "PRED",
                          "inv": "INV"}[f],
                "yn_kind": {"yn_thr": "threshold", "yn_act": "action_rule"}.get(f),
                "comparator": L.CMP_CLASS.get(S["thr"]["op"]) if f == "yn_thr" else None,
                "direction": L.CMP_DIR.get(S["thr"]["op"]) if f == "yn_thr" else None,
                "placement": info.get("placement") if f == "yn_thr" else None,
                "d_steps": CM.fstr(info["d_steps"]) if f == "yn_thr" and info.get("d_steps") is not None else None,
                "polarity": (S["thr"]["neg"] if f == "yn_thr" else S["act"]["neg"]) if yn else None,
                "k_syn": k_syn, "k_all": k_all, "representation": sorted(_reps(S)),
                "t_repr": _trep(S, info) if f == "yn_thr" else None, "world": S["world"],
                "n_unknown": len(SA.unknown_slots(S)), "yes_is_bad": SP._yes_is_bad(card, S) if yn else None,
                "distractor_errors": ex["dmap"] or None, "render_hash": H.render_hash(S),
                "n_options": 2 if yn else len(raw["options"]), "sem_ids": [SS.base_id(k) for k in ex["sems"]],
                "card_version": plan["version"], "subset_class": info.get("subset_class"),
                "tier_step": info.get("tier_step"), "masked": card["label_form"], "card_size": card["size"],
                "gold_answer": _jsonable(ex["sol"]["ans"]), "ntok": ex["ntok"], "unit_id": unit_id,
                "flip_kind": S.get("_flip"), "edge_row": info.get("edge_row"),
                "evidence_changes": info.get("evidence_changes"), "hl": S.get("hl"),
                "gold_probs_exact": {k: CM.fstr(v) for k, v in ex["gold_probs"].items()} if ex["gold_probs"] else None}
        return row, side


def _jsonable(a):
    if isinstance(a, tuple):
        return list(a)
    if isinstance(a, bool) or a is None or isinstance(a, (int, str)):
        return a
    return str(a)


def _reps(S: dict) -> set:
    out = set()
    for e in S["ents"]:
        b = e.get("bay")
        if b:
            if b["form"] == "rates":
                out.add(b["rep"]["base"])
                out.add(b["rep"]["lik"])
            else:
                out.add("count" if b["form"] in ("counts", "nE") else "pct0")
        for o in e.get("outs") or []:
            if o.get("prep"):
                out.add(o["prep"])
        if e.get("ch") is not None and e["ch"].get("rep"):
            out.add(e["ch"]["rep"])
        if e.get("en") is not None:
            out.add(e["en"]["rep"])
        if e.get("mat") is not None:
            out.add(e["mat"]["rep"])
    return {x for x in out if x}


def _trep(S: dict, info: dict):
    tr = S["thr"].get("trep") or {}
    T = S["thr"]["T"]
    digits = len(str(abs(T.numerator))) if T.denominator == 1 else None
    tz = 0
    if T.denominator == 1 and T != 0:
        n = abs(T.numerator)
        while n % 10 == 0:
            tz += 1
            n //= 10
    return {"rep": tr.get("rep") or info.get("qt"), "denom": tr.get("denom"), "digits": digits,
            "trailing_zeros": tz, "T": CM.fstr(T)}


GIT_SHA = None


# ------------------------------------------------------------------------------------------------ units
FORM_OF = {"yn": "yn_thr", "bin": "bin", "tier": "tier", "mat": "mat", "rank_top": "rank_top",
           "rank_order": "rank_order", "dec": "dec", "pred": "pred", "inv": "inv"}


def _inert_for(card, pack, S, rng):
    labs = set()
    for e in S["ents"]:
        if e.get("bay"):
            labs |= set(e["bay"]["hyps"]) | set(e["bay"]["signs"])
    cand = [x for x in pack["inert"] if not any(l.lower() in x.lower() for l in labs)]
    return rng.choice(cand) if cand else None


class UnitMaker:
    def __init__(self, B: Builder, card: dict):
        self.B = B
        self.card = card
        self.pack = B.packs[card["pack"]]
        self.rng = CM.rng_for(B.tag, "planner", card["card_id"])
        self.pl = plans.CardPlanner(card, self.rng)
        self.neg_gold = plans.Cycle(self.rng, [True, False])
        self.pending = {}
        self.seq = 0

    def _rid(self):
        self.seq += 1
        return f"c_f8-{self.B.mode}-{self.card['card_id']}-{self.seq:04d}"

    def structure(self, form, plan, rng, tries=80):
        gen = SP.GEN[form]
        for _ in range(tries):
            try:
                S, info = gen(self.card, self.pack, plan, rng)
            except SP.Retry:
                continue
            except (SA.Undetermined, ValueError, ZeroDivisionError, KeyError, IndexError):
                self.B.stats["gen_exc"] += 1
                continue
            S["_place"] = plan.get("place")
            return S, info
        return None, None

    def _plan(self, form, *, neg_words=False, world=None, gold=None, version=None, single=False):
        if form in ("yn_thr", "yn_act"):
            return self.pl.yn(form, neg=0, world=world, neg_words=neg_words, gold=gold, version=version,
                              single=single)
        p = self.pl.choice(form, world=world)
        if version is not None and p["version"] != version:
            p["version"] = version
        return p

    def anchor(self, form, rng, *, neg_words=False, world=None, version=None, gold=None, single=False,
               rounds=14):
        """One anchor row (repair r1, plan fidelity). The plan is drawn ONCE from the card's quota cycles and kept:
        only its numbers are redrawn (draw order 8). A plan is never swapped for another class (gold, slot, abstain
        slot, option bucket, world, TIER step, placement, comparator, parity, edge), so rejections cannot tilt any
        10.1 distribution; a plan that stays infeasible is logged and the unit is dropped (class_fail stats)."""
        B = self.B
        key = (form, neg_words, world, version, single)
        plan = self.pending.pop(key, None)
        if plan is None:
            plan = self._plan(form, neg_words=neg_words, world=world, gold=gold, version=version, single=single)
        if plan is None:
            return None
        for _ in range(rounds):
            S, info = self.structure(form, plan, rng, tries=12 if form == "inv" else 40)
            if S is None:
                B.stats[f"plan_fail:{form}"] += 1
                continue
            rid = self._rid()
            inert = _inert_for(self.card, self.pack, S, rng) if (
                self.card["sampler"] in ("S1", "S4") and rng.randrange(100) < 30) else None
            out = B.check_and_render(self.card, S, info, plan, rng, row_id=rid, inert=inert)
            if out is not None:
                return S, info, plan, rid, out
            self.seq -= 1
        # the failed plan is handed to the next unit of the same kind (same class, fresh numbers), up to 6 times, so a
        # rarely feasible class keeps its planned share instead of being replaced by the next cycle value
        plan["_retry"] = plan.get("_retry", 0) + 1
        if plan["_retry"] <= 6:
            self.pending[key] = plan
            B.stats[f"plan_retry:{form}"] += 1
        else:
            B.stats[f"class_fail:{form}:{_plan_class(plan)}"] += 1
        return None

    def make(self, utype: str) -> list:
        """Rows (row, sidecar) and relations for one unit."""
        B = self.B
        card = self.card
        form = FORM_OF[card["schema"]]
        rng = CM.rng_for(B.tag, "unit", card["card_id"], self.seq, utype)
        if form == "yn_thr" and card["rules"].get("arules") and rng.randrange(100) < 30:
            form = "yn_act"
        if utype in ("neg2", "neg3"):
            a = self.anchor(form, rng, neg_words=True, world="closed", version="full", gold=self.neg_gold.next())
            if a is None:
                return []
            S, info, plan, rid, (raw, fld, ex) = a
            unit_id = rid
            call = rid + "-u"
            wid = None
            out = [B.record(card, S, info, plan, raw, fld, ex, row_id=rid, call_id=call, seed=CM.h64(rid),
                            unit_id=unit_id, wording_id=_wid(raw, B))]
            rels = []
            for k in ([1] if utype == "neg2" else [1, 2]):
                T = copy.deepcopy(S)
                if form == "yn_thr":
                    T["thr"]["neg"] = k
                else:
                    T["act"]["neg"] = k
                rid2 = self._rid()
                res = B.check_and_render(card, T, info, plan, rng, row_id=rid2,
                                         style_pref=raw["meta"]["format_style"], allow_dup=True)
                if res is None:
                    self.seq -= 1
                    break
                raw2, fld2, ex2 = res
                out.append(B.record(card, T, info, plan, raw2, fld2, ex2, row_id=rid2, call_id=call,
                                    seed=CM.h64(rid2), unit_id=unit_id, wording_id=_wid(raw2, B)))
                rels.append({"a": rid, "b": rid2, "type": "complement" if k == 1 else "equiv"})
            return [("rows", out), ("rels", rels)]
        if utype == "flip" and form == "inv":
            utype = "single"      # one-number INV flips move gold to or from 'None of these', tilting its 1/n rate
        if utype == "flip":
            a = self.anchor(form, rng, world="closed", single=True)
            if a is None:
                return []
            S, info, plan, rid, (raw, fld, ex) = a
            out = [B.record(card, S, info, plan, raw, fld, ex, row_id=rid, call_id=rid, seed=CM.h64(rid),
                            unit_id=rid, wording_id=_wid(raw, B))]
            holder = {}

            def accept(T):
                if T["form"] == "rank_order":
                    g0 = RD.gold_key(S, SA.solve(S)["ans"])
                    g1 = RD.gold_key(T, SA.solve(T)["ans"])
                    if "NOTA" in (g0, g1):
                        return False
                rid2 = self._rid()
                info2 = dict(info)
                if T["form"] == "yn_thr":
                    v = SA.quantity(T, T["ents"][T["case"]], T["q"], SA.CV())
                    import draws as D
                    step = D.STEP[SP.qtype_of(card, T["q"])]
                    d = (v - T["thr"]["T"]) / step
                    if 1 < abs(d) < 2:
                        self.seq -= 1
                        return False
                    info2["d_steps"] = d
                    info2["placement"] = "exact" if d == 0 else ("near" if abs(d) <= 1 else "far")
                res = B.check_and_render(card, T, info2, plan, rng, row_id=rid2,
                                         style_pref=raw["meta"]["format_style"])
                if res is None:
                    self.seq -= 1
                    return False
                holder["r"] = (rid2, info2, res)
                return True
            T = TW.flip_twin(S, card, rng, accept)
            if T is not None:
                rid2, info2, (raw2, fld2, ex2) = holder["r"]
                out.append(B.record(card, T, info2, plan, raw2, fld2, ex2, row_id=rid2, call_id=rid2,
                                    twin_of=rid, twin_kind="flip", seed=CM.h64(rid2), unit_id=rid,
                                    wording_id=_wid(raw2, B)))
            else:
                B.stats["flip_twin_fail"] += 1
            return [("rows", out), ("rels", [])]
        # single (possibly open, possibly with a world twin)
        a = self.anchor(form, rng, single=True)
        if a is None:
            return []
        S, info, plan, rid, (raw, fld, ex) = a
        out = [B.record(card, S, info, plan, raw, fld, ex, row_id=rid, call_id=rid, seed=CM.h64(rid), unit_id=rid,
                        wording_id=_wid(raw, B))]
        if S["world"] == "open" and rng.randrange(3) == 0:
            holder = {}

            def accept(T):
                rid2 = self._rid()
                p2 = dict(plan)
                p2["world"] = "closed"
                info2 = dict(info)
                if T["form"] == "yn_thr":
                    v = SA.quantity(T, T["ents"][T["case"]], T["q"], SA.CV())
                    import draws as D
                    d = (v - T["thr"]["T"]) / D.STEP[SP.qtype_of(card, T["q"])]
                    if 1 < abs(d) < 2:
                        self.seq -= 1
                        return False
                    info2["d_steps"] = d
                    info2["placement"] = "exact" if d == 0 else ("near" if abs(d) <= 1 else "far")
                res = B.check_and_render(card, T, info2, p2, rng, row_id=rid2, style_pref=raw["meta"]["format_style"])
                if res is None:
                    self.seq -= 1
                    return False
                holder["r"] = (rid2, info2, p2, res)
                return True
            target = None
            sol = ex["sol"]
            if not sol["det"] and form != "inv":
                cand = [x for x in (sol.get("set") or []) if x not in ("UNDEF", "CBD")]
                target = rng.choice(cand) if cand else None
            if form == "inv":
                target = "NOTA" if sol["ans"] == "CBD" else sol["ans"]
            T = TW.world_twin(S, card, rng, accept, target=target)
            if T is not None:
                rid2, info2, p2, (raw2, fld2, ex2) = holder["r"]
                out.append(B.record(card, T, info2, p2, raw2, fld2, ex2, row_id=rid2, call_id=rid2, twin_of=rid,
                                    twin_kind="world", seed=CM.h64(rid2), unit_id=rid, wording_id=_wid(raw2, B)))
            else:
                B.stats["world_twin_fail"] += 1
        return [("rows", out), ("rels", [])]


def _plan_class(p: dict) -> tuple:
    n = p.get("n")
    bucket = None if n is None else (0 if n <= 4 else (1 if n <= 9 else (2 if n <= 19 else 3)))
    return (p.get("form"), p.get("slot"), bucket, p.get("world"), p.get("step"), p.get("gold"), p.get("place"),
            p.get("cmpcls"), p.get("neg"), p.get("items"), p.get("version"), p.get("edge_row"))


def _wid(raw, B):
    t = raw["instructions"]
    for wid, w in B.T.wmap.items():
        if w["text"] in t:
            return wid
    return None


def unit_plan(card: dict, n_target: int, rng) -> list:
    """Unit types for one card: label-flip pairs ~11% of rows as anchors (22% of rows in twin sets), negation units on
    YN cards (3-row: 3% of YN rows doubly negated; 2-row: about 9%), singles for the rest."""
    yn = card["schema"] == "yn"
    n3 = round(n_target * 0.03) if yn else 0
    n2 = round(n_target * 0.09) if yn else 0
    nf = 0 if card["schema"] == "inv" else round(n_target * 0.14)
    units = ["neg3"] * n3 + ["neg2"] * n2 + ["flip"] * nf
    rng.shuffle(units)
    return units


def build_card_rows(B: Builder, card: dict, n_target: int):
    if "_examples" not in card:
        prepare_examples(B, card)
    um = UnitMaker(B, card)
    rng = CM.rng_for(B.tag, "unitplan", card["card_id"])
    queue = unit_plan(card, n_target, rng)
    rows, sides, rels, units = [], [], [], []
    guard = 0
    # repair r2: low-yield cards (inv/rank_order on S3: most draws fail ci_missing / long_row / no_named_error) stopped
    # at 6 tries a row and fell short of their planned size; allow up to GUARD_MULT tries a row (cards that reach
    # their target stop as before, so their rows are unchanged)
    while len(rows) < n_target and guard < n_target * GUARD_MULT:
        guard += 1
        ut = queue.pop() if queue else "single"
        res = um.make(ut)
        if not res:
            B.stats[f"unit_fail:{ut}"] += 1
            continue
        r = dict(res)
        if not r["rows"]:
            continue
        units.append([x[0]["id"] for x in r["rows"]])
        for row, side in r["rows"]:
            rows.append(row)
            sides.append(side)
        rels += r["rels"]
    return rows, sides, rels, units


def run(mode: str, cards: list, targets: dict, tag: str, tools: Tools, log_every: int = 5):
    B = Builder(tools, mode, tag)
    allrows, allsides, allrels, allunits = [], [], [], []
    t0 = time.time()
    for i, card in enumerate(cards):
        n = targets[card["card_id"]]
        rows, sides, rels, units = build_card_rows(B, card, n)
        allrows += rows
        allsides += sides
        allrels += rels
        allunits += units
        if (i + 1) % log_every == 0 or i + 1 == len(cards):
            CM.progress(f"{mode}: {i + 1}/{len(cards)} cards, {len(allrows)} rows, "
                        f"{int(time.time() - t0)} s, parse_fail {sum(B.parse_fail.values())}")
    return B, allrows, allsides, allrels, allunits


# ------------------------------------------------------------------------------------------------ worked examples
def example_text(card: dict, S: dict, row_q: str, options: list | None) -> str:
    """Compact case text of a worked example: its fact sentences, then the question (and the options on choice
    examples). Sentences come from the same templates as rows; the example passed the full row checks first."""
    sents = []
    for e in S["ents"]:
        fs, _ = RD.ent_facts(card, S, e, 0, fields=False)
        sents += fs
        b = e.get("bay")
        if b and b["form"] == "counts" and card["sampler"] == "S3":
            s0 = b["signs"][0]
            for j, h in enumerate(b["hyps"]):
                a, bb = b["cnt"][s0][j]
                sents.insert(0, RD.S_("cnt", 0, H=h, E=s0, a=a, b=bb, cases=card["case"]["plural"],
                                      case=card["case"]["noun"], ID=e["id"]))
    txt = " ".join(sents) + "\n" + row_q
    if options:
        txt += "\nOptions: " + "; ".join(options) + "."
    return txt


def prepare_examples(B: Builder, card: dict) -> None:
    """One-line + example and few-shot cards (10.4): examples are structures drawn by the same sampler under the
    card's conventions, labelled by solver A, and passed through every row check (solver B, G3, CI lint) as rows of
    that card before their text is placed in the card."""
    card["_examples"] = None
    card["_example_ids"] = set()
    card["_example_hashes"] = []
    k = card.get("fewshot", 0)
    if not k:
        return
    if card["schema"] != "yn" and card.get("chars", 0) > 2300:
        return          # the moved card block is already near the length budget (instructions print twice)
    if card["schema"] != "yn":
        k = 1
    if card["schema"] in ("rank_order", "inv"):
        return          # option lists of these forms are too long to repeat inside a card under the 2,000 cap
    um = UnitMaker(B, card)
    form = FORM_OF[card["schema"]]
    out = []
    for t in range(k * 30):
        if len(out) >= k:
            break
        rng = CM.rng_for(B.tag, "example", card["card_id"], t)
        plan = um._plan(form, world="closed")
        if plan is None:
            continue
        plan["version"] = "full"
        S, info = um.structure(form, plan, rng)
        if S is None:
            continue
        res = B.check_and_render(card, S, info, plan, rng, row_id=f"example-{card['card_id']}-{t}")
        if res is None:
            continue
        raw, fld, ex = res
        q = fld["_q"]
        # options are listed only where they are not the card's own scale (bins, tiers, ratings, outcomes)
        opts = None if raw["qtype"] == "noul" or form in ("bin", "tier", "mat", "pred") else \
            [t_ for t_, _ in RD.options_for(card, S)]
        ans = raw["gold"] if raw["qtype"] == "choice" else ("Yes" if raw["gold"] == 1 else "No")
        txt = example_text(card, S, q, opts)
        if len(txt) > (700 if card["schema"] == "yn" else 450):
            continue
        out.append({"case": txt, "answer": ans})
        card["_example_ids"] |= {e["id"] for e in S["ents"]}
        card["_example_hashes"].append(H.problem_hash(S))
    card["_examples"] = out or None
    B.stats["examples"] += len(out)


# ------------------------------------------------------------------------------------------------ main
def _trim(rows, sides, rels, units, target):
    """Drop whole single-row units (never twins or negation units) from the largest cards until total == target."""
    if len(rows) <= target:
        return rows, sides, rels, units
    by_id = {r["id"]: i for i, r in enumerate(rows)}
    per_card = collections.Counter(r["meta"]["card_id"] for r in rows)
    drop = set()
    singles = [u for u in units if len(u) == 1]
    need = len(rows) - target
    singles.sort(key=lambda u: (-per_card[rows[by_id[u[0]]]["meta"]["card_id"]], u[0]))
    for u in singles:
        if need <= 0:
            break
        cid = rows[by_id[u[0]]]["meta"]["card_id"]
        if per_card[cid] <= 10:
            continue
        drop.add(u[0])
        per_card[cid] -= 1
        need -= 1
    rows2 = [r for r in rows if r["id"] not in drop]
    sides2 = [x for x in sides if x["id"] not in drop]
    units2 = [u for u in units if not (len(u) == 1 and u[0] in drop)]
    return rows2, sides2, rels, units2


def main(argv=None):
    global GIT_SHA
    import subprocess
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["cand", "qc", "dev"], required=True)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--mr", action="store_true")
    ap.add_argument("--cards", default="", help="repair r2: rebuild only these card ids (comma list) into the patch "
                                                 "shard <mode>_shardpatch; merge.py then replaces those cards' rows")
    a = ap.parse_args(argv)
    import os
    GIT_SHA = os.environ.get("F8_GIT_SHA")          # set by tmp/build_all.sh (the cloud runner has no git)
    if not GIT_SHA:
        GIT_SHA = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                                 cwd=str(CM.LEAN)).stdout.strip()
    si, sn = (int(x) for x in a.shard.split("/"))
    if a.mode == "dev":
        cards = cardbuild.build_all(CP.plan_s5_cards())
        targets = {c["card_id"]: c["n_cand"] for c in cards}
    else:
        cards = cardbuild.build_all(CP.plan_cards())
        if a.mode == "cand":
            targets = {c["card_id"]: c["n_cand"] for c in cards}
        else:
            import math
            targets = {c["card_id"]: math.ceil(c["n_cand"] * 5000 / CP.CANDIDATE_TOTAL * 1.05) for c in cards}
    if a.cards:
        want = set(a.cards.split(","))
        cards = [c for c in cards if c["card_id"] in want]
        assert {c["card_id"] for c in cards} == want, "unknown card id"
    else:
        cards = [c for i, c in enumerate(cards) if i % sn == si]
    tools = Tools()
    CM.progress(f"build {a.mode} shard {a.shard}: {len(cards)} cards, target {sum(targets[c['card_id']] for c in cards)} "
                f"rows, git {GIT_SHA[:8]}")
    B = Builder(tools, a.mode, {"cand": "cand-r1", "qc": "qc-r1", "dev": "dev-s5"}[a.mode])
    B.mr_on = a.mr
    allrows, allsides, allrels, allunits = [], [], [], []
    t0 = time.time()
    for i, card in enumerate(cards):
        rows, sides, rels, units = build_card_rows(B, card, targets[card["card_id"]])
        allrows += rows
        allsides += sides
        allrels += rels
        allunits += units
        print(f"{CM.now()} {a.mode} {a.shard}: card {card['card_id']} ({card['schema']}/{card['sub']}/"
              f"{card['sampler']}) {len(rows)}/{targets[card['card_id']]} rows; total {len(allrows)}; "
              f"{int(time.time() - t0)} s", flush=True)
    tag = f"{a.mode}_shardpatch" if a.cards else f"{a.mode}_shard{si}of{sn}"
    d = CM.TMP / "shards"
    d.mkdir(parents=True, exist_ok=True)
    CM.write_jsonl(d / f"{tag}.rows.jsonl", allrows)
    CM.write_jsonl(d / f"{tag}.side.jsonl", allsides)
    CM.write_jsonl(d / f"{tag}.rels.jsonl", allrels)
    stats = {"stats": dict(B.stats), "parse_fail": dict(B.parse_fail),
             "mr": [[list(k) if isinstance(k, tuple) else k, v] for k, v in B.mr.items()], "mr_fail": B.mr_fail,
             "units": allunits, "examples": {c["card_id"]: {"n": len(c.get("_examples") or []),
                                                           "hashes": c.get("_example_hashes") or []} for c in cards}}
    with open(d / f"{tag}.stats.json", "w") as f:
        json.dump(stats, f)
    CM.progress(f"build {a.mode} shard {a.shard} done: {len(allrows)} rows, parse_fail {sum(B.parse_fail.values())}, "
                f"{int(time.time() - t0)} s")


if __name__ == "__main__":
    main()
