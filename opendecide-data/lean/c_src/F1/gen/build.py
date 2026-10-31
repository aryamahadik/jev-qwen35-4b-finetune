"""F1 round-1 build driver.

  python build.py cards                 # plan + build the 120 training cards (+ held-out dev cards), fit check
  python build.py rows <set> [n_proc]   # set = cand | qc ; rows per card, gates inline, shards in tmp/shards_<set>/
  python build.py dev [n_proc]          # S5 items (400) + depth sweep (300) on held-out packs and held-out styles
  python build.py merge <set>           # shards -> out/<file>.jsonl (+ relations, sidecar)

Progress lines go to lean/c_build/progress_phase2.log ([F1] prefix); details to tmp/build.log.
"""
from __future__ import annotations

import hashlib
import json
import os
import pickle
import random
import sys
import time
import traceback
from collections import Counter, defaultdict
from multiprocessing import Pool

import common as C
from common import OUT, TMP, log, progress, read_jsonl, write_jsonl

CARDS_PKL = TMP / "cards_r1.pkl"



def _load_cards():
    """Cards with the r1.1 balanced per-card yes rates (yplan.py) applied to the training Q3 cards."""
    import yplan
    with open(CARDS_PKL, "rb") as f:
        D = pickle.load(f)
    # r2 card patch (cardfix_r2.py): Q1 default / CBD label choice (longest option per gold source) and the rows-per-card
    # refit (amendment shares). r2: applied before the y plan, which now plans on the r2 rows (yplan_weights_r2.json)
    import cardfix_r2
    info = cardfix_r2.apply(D["cards"])
    # the card statements and illustrations were rendered at card build; re-render them on the patched cards (the
    # construct set and its fit are kept; worked cases exist only on Q3 cards, which the patch never touches)
    patched = {cid for cid, _ in info.get("changed", [])}
    if patched:
        from packs_f1 import load_all
        allp = load_all()
        for c in D["cards"]:
            if c["card_id"] in patched:
                _refresh_statements(c, allp[c["pack_id"]])
    try:
        (TMP / "repair").mkdir(exist_ok=True)
        json.dump(info, open(TMP / "repair" / "cardfix_r2.json", "w"), indent=0, sort_keys=True, default=str)
    except OSError:
        pass
    p = yplan.apply(D["cards"])
    try:
        json.dump(p, open(TMP / "repair" / "yplan_r2.json", "w"), indent=0, sort_keys=True)
    except OSError:
        pass
    return D

def _refresh_statements(card, pack):
    """r2: statements and illustrations of a card patched at load (cardfix_r2); illustrations pass the same G3 check."""
    import illus as IL
    import parse_f1 as PF
    from cards import card_statements, statement_rows
    card["_stmts"] = card_statements(card)
    if card["defs"] == "one_line_examples":
        ill, _ = IL.make_illustrations(card, pack, statement_rows(card))

        def fac(decl):
            P = PF.Parser.__new__(PF.Parser)
            P.subj = "case"
            P.problems = []
            P.setup_lexicon(decl)
            return P
        n = 0
        for row, txts in ill.items():
            for t in txts:
                IL.check_illustration(t, card, pack, fac)
                n += 1
        card["illus"] = ill
        card["illus_checked"] = n
    return card


def _card_extras(card, pack):
    """Illustrations, worked cases, statements; G3 checks on illustrations and worked cases."""
    import illus as IL
    import parse_f1 as PF
    from cards import card_statements, statement_rows
    card["_stmts"] = card_statements(card)
    card["illus"] = {}
    card["illus_checked"] = 0
    if card["defs"] == "one_line_examples":
        ill, _ = IL.make_illustrations(card, pack, statement_rows(card))

        def fac(decl):
            P = PF.Parser.__new__(PF.Parser)
            P.subj = "case"
            P.problems = []
            P.setup_lexicon(decl)
            return P
        for row, txts in ill.items():
            for t in txts:
                IL.check_illustration(t, card, pack, fac)
                card["illus_checked"] += 1
        card["illus"] = ill
    if card["defs"] != "short":
        from cards import fit_constructs
        fit_constructs(card, pack)
        card["_stmts"] = card_statements(card)
        if card["defs"] == "one_line_examples":
            ill, _ = IL.make_illustrations(card, pack, statement_rows(card))
            card["illus"] = ill
    card["few_cases"] = None
    if card["fewshot"]:
        wc = IL.make_worked_cases(card, pack)
        for txt, ans, _ in wc:
            IL.check_worked_case(txt, ans, card, pack)
        card["few_cases"] = [{"case": t, "answer": a} for t, a, _ in wc]
        card["fewshot_template"] = IL.FEWSHOT_TEMPLATES[int(C.unit("ft", card["card_id"]) *
                                                           len(IL.FEWSHOT_TEMPLATES))]
        card["_worked_structs"] = [x for _, _, x in wc]
    return card


def fit_check(card, pack, held_out=False):
    """Section 1: the card's smallest draw (3 rules, no notice, 4 fields, smallest option count) <= 1,400 tokens."""
    import emit as EM
    import rows as R
    import samplers as SM
    import solver_a as A
    rng = C.rng_for("fit", card["card_id"])
    c2 = dict(card)
    c2["constructs"] = {x for x in card["constructs"] if x not in ("notices", "inert")}
    best = None
    for t in range(60):
        try:
            attrs, k2r = SM.row_attrs(c2, pack, rng, n_target=4)
            attrs = SM.add_distractors(attrs, c2, rng, n=1)
            pol = SM.make_policy(c2, attrs, k2r)
            if card["sampler"] == "S3":
                rules, lm = SM.draw_table_rules(attrs, c2, rng)
                rules = rules[:3]
            else:
                rules, lm = SM.draw_rules(attrs, c2, rng, n_rules=3, plain=card["short"])
            S = SM.Struct(attrs=attrs, rules=rules, notices=[], inert=[], policy=pol)
            SM.set_order(S, c2, rng, card["sampler"] if card["sampler"] != "S5" else "S1")
            if card["sampler"] == "S3":
                S.s3_rows = [r.rid for r in rules]
            case = SM.draw_case(S, c2, rng, ref="FIT-0001")
            if card["qtype"] == "Q4":
                cases = [SM.draw_case(S, c2, rng, ref=f"FIT-000{i}") for i in range(3)]
                for c_ in cases:
                    c_.unknown = frozenset()
                    c_.notrec = frozenset()
                refs = ["Case A2", "Case B3", "Case C4"]
                for c_, r_ in zip(cases, refs):
                    c_.ref = r_
                row = {"S": S, "cases": cases, "q": {"qtype": "Q4", "X": card["outcomes"][0]},
                       "options": refs + (["__NONE__"] if card["none_card"] else []), "gold": refs[0],
                       "q4_refs": refs}
            elif card["qtype"] == "Q3":
                row = {"S": S, "cases": [case], "q": {"qtype": "Q3", "X": card["outcomes"][0], "pol": "aff",
                                                     "frame": 0, "ref_text": f"{card['subj']} {case.ref}"}, "gold": 1}
            elif card["qtype"] == "Q1":
                opts = list(card["outcomes"]) + ([A.CBD] if card["world"] == "open" else [])
                row = {"S": S, "cases": [case], "q": {"qtype": "Q1", "ref_text": f"{card['subj']} {case.ref}"},
                       "options": opts, "gold": opts[0]}
            else:
                outs = card["outcomes"]
                opts = [(o, r.rid) for o in outs for r in rules][:10]
                if len(opts) < 10:
                    opts += [(o, "D") for o in outs][:10 - len(opts)]
                row = {"S": S, "cases": [case], "q": {"qtype": "Q2", "ref_text": f"{card['subj']} {case.ref}"},
                       "options": opts, "gold": opts[0]}
            case.unknown = frozenset() if card["qtype"] == "Q4" else case.unknown
            fields, must, st, wid, opts_t, gold, canon_opts, qtext = EM.render_row(card, pack, row, f"fit-{t}",
                                                                                    held_out=held_out)
            out = {"id": f"fit-{card['card_id']}-{t}", "qtype": "noul" if card["qtype"] == "Q3" else "choice",
                   "options": opts_t, "gold": gold, **fields}
            n = EM.prompt_len(out)
            best = n if best is None else min(best, n)
            if best is not None and t >= 4:
                break
        except Exception:
            continue
    return best


FIT_TARGET = 1400
FIT_RELAXED = 1700
FIT_RELAXED_Q2 = 1800


def fit_card(c0, pack):
    """Section 1 fit: redraw (reduce) the construct set and definition style together until the card's smallest draw
    is <= 1,400 tokens. Phase A (towards 1,400): one worked case, one illustrated row, redundant operator forms
    dropped (cards.DROP_ORDER; F1-core constructs are kept). Phase B: when 1,400 is out of reach (A16.1 prints the
    answer group and the options twice on choice rows), the card is kept if its smallest draw is <= 1,800 tokens
    (Q2: 1,900) and flagged fit_relaxed. Phase C (only above that bound): drop the worked case, switch the
    examples style to one-line, then drop core constructs in a fixed order. Every row stays < 2,000 tokens."""
    import cards as CD
    from cards import card_statements

    def refresh():
        c0["_stmts"] = card_statements(c0)
        return fit_check(c0, pack)
    ln = fit_check(c0, pack)
    lim = FIT_RELAXED_Q2 if c0["qtype"] == "Q2" else FIT_RELAXED
    # phase A
    while ln is None or ln > FIT_TARGET:
        if c0.get("few_cases") and len(c0["few_cases"]) > 1:
            c0["few_cases"] = c0["few_cases"][:1]
            c0["_worked_structs"] = c0["_worked_structs"][:1]
        elif c0["defs"] == "one_line_examples" and len(c0.get("illus") or {}) > 1:
            keep = sorted(c0["illus"])[:1]
            c0["illus"] = {k: c0["illus"][k] for k in keep}
        else:
            cs = set(c0["constructs"])
            dropped = False
            for c in CD.DROP_ORDER:
                if c not in cs:
                    continue
                if c.startswith("num_") and len([x for x in cs if x.startswith("num_")]) <= 1:
                    continue
                cs.discard(c)
                dropped = True
                break
            if not dropped:
                break
            c0["constructs"] = cs
        ln = refresh()
    if ln is not None and ln <= FIT_TARGET:
        c0["fit_tokens"] = ln
        return ln, c0
    c0["fit_relaxed"] = True
    # phase C (only above the relaxed bound)
    order = ["fewshot", "style", "inert", "last", "xor", "kofn", "all", "any", "or", "onlyif", "unless", "exc2",
             "replace"]
    for step in order:
        if ln is not None and ln <= lim:
            break
        if step == "fewshot":
            if not c0.get("few_cases"):
                continue
            c0["few_cases"], c0["fewshot"] = None, False
        elif step == "style":
            if c0["defs"] != "one_line_examples":
                continue
            c0["defs"], c0["illus"] = "one_line", {}
        else:
            cs = set(c0["constructs"])
            if step not in cs:
                continue
            if step == "replace" and c0["sampler"] == "S6" and len(cs & {"replace", "insert", "repeal"}) <= 1:
                continue
            cs.discard(step)
            c0["constructs"] = cs
            c0["core_dropped"] = c0.get("core_dropped", []) + [step]
        ln = refresh()
    c0["fit_tokens"] = ln
    return ln, c0


def build_cards(n_cards=120):
    import cards as CD
    from packs_f1 import load_all, split_packs
    allp = load_all()
    train, held = split_packs()
    specs = CD.plan_cards(n_cards)
    order = CD.assign_packs(specs, train)
    cards = []
    used_packs = set()
    pi = 0
    fit_log = []
    for s in specs:
        card = None
        tries = 0
        while card is None and tries < 12:
            tries += 1
            while order[pi] in used_packs:
                pi += 1
            pid = order[pi]
            pi += 1
            c0 = CD.build_card(s, allp[pid])
            if c0 is None:
                continue
            used_packs.add(pid)
            try:
                c0 = _card_extras(c0, allp[pid])
            except Exception as e:
                log(f"card {s['card_id']} extras failed on {pid}: {e}")
                continue
            ln, c0 = fit_card(c0, allp[pid])
            lim = FIT_RELAXED_Q2 if c0["qtype"] == "Q2" else FIT_RELAXED
            redraw = 0
            while (ln is None or ln > lim) and redraw < 4:
                redraw += 1
                rng = C.rng_for("cons-redraw", s["card_id"], pid, redraw)
                c0["constructs"] = CD.draw_constructs({**s}, allp[pid], rng)
                c0 = _card_extras(c0, allp[pid])
                ln, c0 = fit_card(c0, allp[pid])
            fit_log.append((s["card_id"], pid, ln, c0.get("fit_relaxed", False)))
            if ln is None or ln > (FIT_RELAXED_Q2 if c0["qtype"] == "Q2" else FIT_RELAXED):
                log(f"card {s['card_id']} fails fit check on {pid} ({ln})")
                continue
            c0["fit_tokens"] = ln
            card = c0
        if card is None:
            raise SystemExit(f"card {s['card_id']} could not be built")
        cards.append(card)
    # held-out dev cards (S5 + depth sweep): one per held-out pack, never trained
    dev = []
    import copy
    for j, pid in enumerate(held):
        u = allp[pid]
        base = dict(specs[j % len(specs)])
        base = {**base, "card_id": f"F1-D{j + 1:03d}", "sampler": "S5", "short": False, "label_form": "plain",
                "fewshot": False, "defs": ["one_line", "decision_list", "one_line"][j % 3],
                "qtype": ["Q3", "Q1", "Q3", "Q2", "Q1"][j % 5], "world": ["closed", "open", "closed", "missing",
                                                                            "closed"][j % 5]}
        if base["world"] == "missing" and base["qtype"] == "Q1":
            base["world"] = "closed"
        if base["prim"] == "ORDER":
            base["prim"], base["sec"] = "SPEC", None
        base["xor"] = False
        base["none_card"] = False
        c0 = CD.build_card(base, u, held_out=True)
        if c0 is None:
            continue
        try:
            c0 = _card_extras(c0, u)
        except Exception:
            continue
        dev.append(c0)
    with open(CARDS_PKL, "wb") as f:
        pickle.dump({"cards": cards, "dev": dev, "fit": fit_log}, f)
    progress(f"cards built: {len(cards)} training cards (packs {len(used_packs)}), {len(dev)} held-out dev cards; "
             f"fit check max {max(c['fit_tokens'] for c in cards)} tokens")
    return cards, dev


# ---------------------------------------------------------------- rows

def _row_json(card, row, rid, gid, call_id, fields, opts, gold, st, wid, shash, plen, role, twin_of, held_out,
              seed_key):
    q = row["q"]
    edge = [f"q:{q['qtype']}", f"label:{card['label_form']}"]
    if q["qtype"] == "Q3":
        edge.append(f"pol:{q['pol']}")
    if row.get("unit_kind"):
        edge.append(f"unit:{row['unit_kind']}")
    if row.get("mr"):
        edge.append(f"mr:{row['mr']}")
    meta = {
        "family": "F1", "spec_id": C.SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack_id"],
        "sampler": card["sampler"], "gen_version": C.GEN_VERSION, "git_sha": GIT, "seed": int(C.unit("seed", rid) *
                                                                                              2 ** 31),
        "structure_hash": shash, "difficulty_bin": None, "crowd_pg": None, "depth": row["depth"],
        "deep": bool(row.get("deep")), "format_style": st["id"], "wording_id": wid, "defs_style": card["defs"],
        "twin_of": twin_of, "twin_kind": row.get("twin_kind"), "text_source": None, "licence": C.LICENCE,
        "edge": edge,
    }
    if card.get("persona_seed"):
        meta["persona_seed"] = card["persona_seed"]
    return {"id": rid, "group_id": gid, "call_id": call_id, "source": C.SOURCE, "state": fields["state"],
            "qtype": "noul" if q["qtype"] == "Q3" else "choice", "instructions": fields["instructions"],
            "options": opts, "gold": gold, "role": role, "card": fields["card"], "meta": meta}


GIT = C.git_sha()


def _sidecar(card, row, rid, gid, plen, k_syn, k_all):
    import solver_a as A
    S = row["S"]
    q = row["q"]
    src = None
    pos = None
    if row.get("res") is not None:
        src, w = A.gold_source(row["res"])
        if src == "ONE":
            el = row["res"]["comps"][0]["rules"][w][2]
            idx = [i for i, x in enumerate(S.order) if x == el]
            pos = idx[0] + 1 if idx else None
    g = None
    if q["qtype"] == "Q4":
        g = "none" if row["gold"] == "__NONE__" else "case"
    elif q["qtype"] in ("Q1",):
        g = row["gold"]
    sc = {"id": rid, "group_id": gid, "qtype": q["qtype"], "world": S.policy.world,
          "policy": S.policy.prim + ("+" + S.policy.sec if S.policy.sec else ""), "tie": S.policy.tie,
          "n_rules": len(S.rules), "n_amend": len(S.notices), "n_elements": len(S.order), "position": pos,
          "gold_source": src, "depth": row["depth"], "deep": bool(row.get("deep")), "A": row.get("A"),
          "boundary": (row.get("info") or {}).get("boundary"), "len_tokens": plen, "k_syn": k_syn, "k_all": k_all,
          "unit_kind": row.get("unit_kind"), "twin_kind": row.get("twin_kind"), "role": row.get("role"),
          "label_form": card["label_form"], "sampler": card["sampler"], "short": card["short"],
          "n_inert": len(S.inert), "attack": bool(row.get("attack"))}
    if q["qtype"] == "Q3":
        X = q["X"]
        bad = card["valence"][X] == "bad"
        sc.update({"pol": q["pol"], "X_role": card["roles"][X], "gold": row["gold"],
                   "yes_bad": (q["pol"] in ("aff", "dneg") and bad) or (q["pol"] == "neg" and not bad),
                   "flips": row.get("flips")})
    if q["qtype"] in ("Q1", "Q2", "Q4"):
        opts = row["options"]
        sc["k"] = len(opts)
        roles = []
        for o in opts:
            oo = o[0] if isinstance(o, tuple) else o
            roles.append("cbd" if oo == A.CBD else "none" if oo == "__NONE__" else card["roles"].get(oo, "case"))
        sc["option_roles"] = roles
        go = row["gold"][0] if isinstance(row["gold"], tuple) else row["gold"]
        sc["gold_role"] = "cbd" if go == A.CBD else "none" if go == "__NONE__" else card["roles"].get(go, "case")
        if q["qtype"] == "Q2":
            sc["gold_basis"] = "code" if isinstance(row["gold"][1], str) else ("rule" if row["gold"][1] else None)
            sc["code_share"] = sum(1 for o in opts if isinstance(o[1], str)) / len(opts)
        if q["qtype"] == "Q1":
            sc["traps"] = [str(x) for x in row.get("traps", [])]
    if row.get("eo"):
        sc["err_models"] = {E: (str(o["q1"]) if o["q1"] is not None else None) for E, o in row["eo"].items()}
    return sc


# r3 pass E (G10 role_rate escalate|Q1, qc -2.42 pp on 5-9 option rows): a Q1 top-up batch is more rows of the same
# card, and the role-rate rule (G0 8) counts every emitted row of the card. A fresh GroupBuilder let the top-up batch
# start from zero counts, so under-drawn roles fell short (pass D qc top-up Q1 rows on 5-9 options: escalate gold 7 vs
# 15.9 expected). The batch's starving check now adds the card's main-shard rows of the same pool (whole-card deficit,
# lower slack TOPUP_SLACK_LO), so the top-up rows close the card's role gap. The over check and the slot balance stay
# on the batch's own rows (whole-card over counts blocked the A28 source quotas of planned top-ups in smoke runs).
Q1_TOPUP_CARRY = {"topup": "shards_cand", "vqctop": "shards_qc"}
TOPUP_SLACK_LO = 0.25


def _carry_rbal():
    import balance as BAL

    class CarryRoleBalance(BAL.RoleBalance):
        SLACK_LO = TOPUP_SLACK_LO

        def __init__(self):
            super().__init__()
            self.c0 = Counter()
            self.e0 = Counter()

        def starving(self, gold_role, shown):
            for ro, mk in shown.items():
                if ro in BAL.SPECIAL and ro != gold_role and \
                        self.cnt[ro] + self.c0[ro] < self.exp[ro] + self.e0[ro] + mk - self.SLACK_LO:
                    return ro
            return None
    return CarryRoleBalance()


def _q1_topup_carry(gb, card, set_name):
    d = Q1_TOPUP_CARRY.get(set_name)
    if d is None or card["qtype"] != "Q1":
        return 0
    p = TMP / d / f"{card['card_id']}.json"
    if not p.exists():
        return 0
    from solver_a import CBD
    inv = {str(card["display"][o]): o for o in card["outcomes"]}
    inv[card["cbd_label"]] = CBD
    rb = _carry_rbal()
    n = 0
    for row in json.load(open(p))["rows"]:
        opts = [inv[x] for x in row["options"]]
        rb.c0[gb.role_of(inv[row["gold"]])] += 1
        for ro, mk in gb.shown_roles(opts).items():
            rb.e0[ro] += mk
        n += 1
    gb.rbal = rb
    return n


# r3 pass E (G6 yes/no view c, card + instructions without the question: gbt 0.533 vs bar 0.5214): a contrast twin is a
# minimal pair of its base row, so on yes/no rows it now shows the base row's surface (instruction wording, card
# format style and render draws) and differs only by its mutation and its flipped answer. Twins with their own
# surface draws gave view c a within-card label signal (simulation on the pass-D qc pool: 0.533 -> 0.487).
TWIN_SURFACE_MATCH_QTYPES = ("Q3",)


def _q1_topup_carry(gb, card, set_name):
    d = Q1_TOPUP_CARRY.get(set_name)
    if d is None or card["qtype"] != "Q1":
        return 0
    p = TMP / d / f"{card['card_id']}.json"
    if not p.exists():
        return 0
    from solver_a import CBD
    inv = {str(card["display"][o]): o for o in card["outcomes"]}
    inv[card["cbd_label"]] = CBD
    n = 0
    for row in json.load(open(p))["rows"]:
        opts = [inv[x] for x in row["options"]]
        gold = inv[row["gold"]]
        gb.rbal.account(gb.role_of(gold), gb.shown_roles(opts))
        gb.q1_counts[gold] += 1
        n += 1
    gb.rbal.SLACK_LO = TOPUP_SLACK_LO
    return n


def gen_card(args):
    """Worker: rows for one card. Returns dict with rows, relations, sidecar, stats."""
    card, pack, target, set_name, held_out = args[:5]
    # r3 pass C (G10 longest per source / role rate / Q2 code share): optional 6th item = Q2 running deviations carried
    # in from the previous Q2 card of the same chain (tmp/rr1/q2chain_r3.py); None = a fresh card (as before)
    carry = args[5] if len(args) > 5 else None
    import emit as EM
    import parse_f1 as PF
    import rows as R
    import solver_a as A
    import negcount
    from fmt1 import card as fcard
    from fmt1.render import FormatError
    from render_f1 import RenderFail
    t0 = time.time()
    tr = R.Trackers()
    gb = R.GroupBuilder(card, pack, tr, f"{set_name}|{card['card_id']}", held_out=held_out)
    if carry:
        # r3 pass C: the per-card dead band of the Q2 keep step (rows.q2_keepf, |dev| <= 0.5 not steered) let every Q2
        # card settle at the same edge (pass B: Q2 T-source longest-gold -9.9 / -6.2 hits over 17 cards in cand / qc);
        # with the deviations carried along a chain of cards the band applies to the chain total, not to each card
        gb.q2dev.update({tuple(k): v for k, v in carry})
    gb.defer_account = True   # r1.1: balance counters book emitted rows only (length / gate drops are not counted)
    # r3 (A28): per-card (gold source, longest) quotas for this set (cardfix_r3_plan.json); the row target follows them
    gb.srcq = (card.get("src_quota") or {}).get(set_name)
    if gb.srcq is not None:
        target = min(target, sum(gb.srcq.values()))
    n_carry = _q1_topup_carry(gb, card, set_name)
    w_rng =random.Random(int(hashlib.sha256(f"F1|wording|{set_name}|{card['card_id']}".encode()).hexdigest(), 16) % 2**32)
    w_bag = []
    vocab = PF.vocab_for(pack)
    out_rows, rels, side = [], [], []
    stats = Counter()
    if n_carry:
        stats["q1_topup_carry_rows"] = n_carry
    gi = 0
    fails = []
    # r2: no deep items on Q2 cards (their rows stay on small structures for the length cap; deep Q2 draws were
    # rejected almost always and cost the card's time budget); the family's deep share stays <= 10% (G0 8)
    deep_quota = 0.0 if card["qtype"] == "Q2" else (0.07 if card["qtype"] != "Q4" else 0.04)
    n_deep = 0
    tmax = float(os.environ.get("F1_CARD_SECS", "1800"))
    # r1.1: low-yield cards (narrow construct sets make the A17 two-trap rule rare) get more group attempts within
    # the same time cap, so every card reaches >= 5 rows (G11: >= 5 wordings per card)
    while len(out_rows) < target and (gi < target * 40 or (getattr(gb, "_relax_gold", False) and len(out_rows) < 8)) \
            and time.time() - t0 < tmax:
        gi += 1
        # r3 (G11: >= 5 wordings per card): a card with almost no rows after 10 x target group attempts (F1-C029: 3 rows
        # from 1,677 attempts, stopped by the attempt cap) drops the per-card Q1 gold steers (slot / role balance) and
        # keeps drawing, only until it holds 8 rows (not sticky, so the steers bind again after that)
        gb._relax_gold = (gi > 10 * target or time.time() - t0 > 0.5 * tmax) and len(out_rows) < min(8, target)
        # r2: a card far behind its row target after half its time drops the r2 depth / amendment quotas (G11: every
        # card shows >= 5 wordings; F1-C029 kept only 4 rows under them)
        if time.time() - t0 > 0.5 * tmax and len(out_rows) < 0.3 * target:
            gb._relaxed = True
        deep = ((n_deep + 1) <= deep_quota * (len(out_rows) + 1) and not card["short"] and gb.dmax() >= 5
                and gb.rng.random() < 0.5)
        try:
            grp = gb.build_group(deep=deep)
        except A.Reject as e:
            stats["group_reject" + ("_deep" if deep else "")] += 1
            if deep:
                try:
                    grp = gb.build_group(deep=False)
                except A.Reject:
                    continue
            else:
                continue
        except Exception as e:
            stats["group_exc:" + type(e).__name__] += 1
            fails.append(("group_exc", card["card_id"], traceback.format_exc(limit=4)[-600:]))
            continue
        gid = f"F1r1{set_name[0]}-{card['card_id']}-{gi:04d}"
        call_u = gid + "-u"
        emitted = []
        acc_rows = []
        unit_n, unit_long = 0, False
        ok_group = True
        suffix = {"base": "b", "variant": "v", "attacked": "a", "twin": "t"}
        base_surface = None
        for k, row in enumerate(grp):
            rid = f"{gid}-{suffix.get(row.get('role'), 'x')}{k}"
            if row.get("role") == "twin" and base_surface is not None and \
                    row["q"]["qtype"] in TWIN_SURFACE_MATCH_QTYPES:
                # r3 pass E: matched twin surface (see TWIN_SURFACE_MATCH_QTYPES)
                row["wording_idx"], row["_surface_key"] = base_surface
            else:
                # r1.1 (G11): wordings are drawn from the card's pool without replacement, the bag refilled and
                # reshuffled when empty (every run of len(pool) rows shows every wording; random order, so no link to
                # the answer plan)
                if not w_bag:
                    w_bag = list(range(len(card["wordings"])))
                    w_rng.shuffle(w_bag)
                row["wording_idx"] = w_bag.pop()
            if k == 0 and row.get("role", "base") == "base":
                base_surface = (row["wording_idx"], rid)
            try:
                fields, must, st, wid, opts, gold, canon_opts, qtext = EM.render_row(card, pack, row, rid,
                                                                                     held_out=held_out)
                outr = {"id": rid, "qtype": "noul" if row["q"]["qtype"] == "Q3" else "choice", "options": opts,
                        "gold": gold, **fields}
                res = fcard.loader_check(outr, must_show=must)
                if not res["ok"]:
                    stats["loader_fail"] += 1
                    fails.append(("loader", rid, res["problems"][:3]))
                    raise EM.GateFail("loader")
                plen = EM.prompt_len(outr)
                if plen >= EM.len_cap(row["q"]["qtype"]):
                    stats[f"len_reject:{row['q']['qtype']}"] += 1
                    if row["q"]["qtype"] == "Q2" and len(opts) >= 20:
                        gb.kplan["big_len_fail"] += 1   # r2: feasibility feedback for the Q2 20-60 option plan
                    gb.kplan["len_fail"] += 1           # r2 pass B: feedback for the deep-need structure size
                    raise EM.GateFail("length")
                shash, parsed = EM.gate_row(card, pack, row, outr, vocab, canon_opts)
            except (EM.GateFail, RenderFail, FormatError, KeyError, ValueError) as e:
                msg = str(e)
                if msg not in ("length",):
                    if not isinstance(e, EM.GateFail) or msg != "loader":
                        stats["gate_fail"] += 1
                        fails.append(("gate", rid, card["sampler"], row["q"]["qtype"], msg[:300]))
                if row.get("role") == "base":
                    ok_group = False
                    break
                continue
            role = row.get("role", "base")
            if role != "twin":
                # r3 (G15, A22 Q2 rows): a relation unit (one call_id) holding a row >= 2,000 tokens keeps <= 2 rows;
                # a unit row past the second is not emitted when the unit (with this row) holds such a row
                if unit_n >= 2 and (unit_long or plen >= EM.LONG_UNIT):
                    stats["unit_row_skipped_long"] += 1
                    continue
                unit_n += 1
                unit_long = unit_long or plen >= EM.LONG_UNIT
            ksyn = kall = None
            if row["q"]["qtype"] == "Q3":
                nc = negcount.count(qtext, affixed=tuple(pack.get("affixed", [])))
                ksyn, kall = nc.k_syn, nc.k_all
            role = row.get("role", "base")
            twin_of = None
            if role == "twin":
                twin_of = emitted[0]["id"] if emitted else None
            call_id = rid if role == "twin" else call_u
            j = _row_json(card, row, rid, gid, call_id, fields, opts, gold, st, wid, shash, plen, role, twin_of,
                          held_out, set_name)
            emitted.append(j)
            acc_rows.append(row)
            sc = _sidecar(card, row, rid, gid, plen, ksyn, kall)
            side.append(sc)
            if row.get("rel") and emitted and role != "base":
                rels.append({"a": emitted[0]["id"], "b": rid, "type": row["rel"]})
        if not ok_group or not emitted:
            side = [s for s in side if s["group_id"] != gid]
            rels = [r for r in rels if not r["a"].startswith(gid)]
            continue
        # a unit with a dropped base never survives; units keep <= 3 rows
        if len(out_rows) + len(emitted) > 128:
            break   # r2: G11 rows per card <= 128 (a last multi-row group made 129 on two cards)
        out_rows += emitted
        for row in acc_rows:
            gb.account_row(row)
        if any(r.get("deep") for r in grp):
            n_deep += len(emitted)
        stats["groups"] += 1
    stats.update({f"builder:{k}": v for k, v in gb.stats.items()})
    return {"card_id": card["card_id"], "rows": out_rows, "rels": rels, "side": side, "stats": dict(stats),
            "fails": fails[:50], "secs": round(time.time() - t0, 1),
            **({"q2dev_end": [[list(k), v] for k, v in sorted(gb.q2dev.items(), key=str)]} if card["qtype"] == "Q2" else {})}


def run_rows(set_name, n_proc=8, only=None):
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    cards = D["cards"]
    if only:
        cards = [c for c in cards if c["card_id"] in only]
    shard_dir = TMP / f"shards_{set_name}"
    shard_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for c in cards:
        if set_name == "cand":
            target = c["n_rows"]
        else:
            target = max(30, int(round(c["n_rows"] * 5200 / 8100)))
        if (shard_dir / f"{c['card_id']}.json").exists():
            continue
        jobs.append((c, allp[c["pack_id"]], target, set_name, False))
    progress(f"rows[{set_name}]: start {len(jobs)} cards, {n_proc} processes")
    t0 = time.time()
    done = 0
    tot = Counter()
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(gen_card, jobs):
            done += 1
            with open(shard_dir / f"{res['card_id']}.json", "w") as f:
                json.dump(res, f, ensure_ascii=False)
            tot.update({k: v for k, v in res["stats"].items() if not k.startswith("builder:")})
            tot["rows"] += len(res["rows"])
            log(f"[{set_name}] {res['card_id']} rows {len(res['rows'])} secs {res['secs']} stats {res['stats']} "
                f"fails {res['fails'][:3]}")
            if done % 10 == 0 or done == len(jobs):
                progress(f"rows[{set_name}]: {done}/{len(jobs)} cards, {tot['rows']} rows, gate_fail "
                         f"{tot['gate_fail']}, loader_fail {tot['loader_fail']}, {int(time.time() - t0)} s")
    return tot


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "cards":
        build_cards()
    elif cmd == "rows":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
        print(run_rows(sys.argv[2], n, only))


# ---------------------------------------------------------------- dev: S5 items + depth sweep

def s5_row(card, pack, gb, rid, vocab):
    """One S5 flowchart item (Q1 / Q3), rendered in a held-out style, checked by gate_s5 and loader_check."""
    import emit as EM
    import rows as R
    import s5 as S5
    import solver_a as A
    from fmt1 import card as fcard
    from render_f1 import Fmt, question
    qt = card["qtype"]
    row = gb.build_q3() if qt == "Q3" else gb.build_q1()
    S = row["S"]
    if len(S5._lits(S)) > 9:
        raise A.Reject("flowchart: too many tests")
    S._s5 = S5.compile_flowchart(S)
    card2 = dict(card)
    stmts = S5.s5_statements(card, S)
    fm = Fmt(card, S)
    rng = C.rng_for("s5render", rid)
    doc = S5.s5_doc(card, S, row["cases"][0], fm, rng, stmts)
    qtext = question(card, row["q"], rng)
    opts, gold, canon = EM.options_and_gold(card, row)
    if qt == "Q3":
        cir = {"title": None, "blocks": [{"type": "items", "items": [t for r, g, t in stmts]}]}
        cir["blocks"].append({"type": "defs", "variant": "DV01", "heading": None,
                              "entries": [{"name": card["display"][o], "text": card["meanings"][o]}
                                          for o in card["outcomes"]]})
    else:
        cir = {"title": None, "blocks": [{"type": "items", "items": [t for r, g, t in stmts if g == "answer"]},
                                         {"type": "defs", "variant": "DV01", "heading": None,
                                          "entries": [{"name": card["display"][o], "text": card["meanings"][o]}
                                                      for o in card["outcomes"]]}]}
    st = EM.pick_style(card, rid, doc, held_out=True, exclude_flags=("rewrites_keys",))
    wid = EM.pick_wording(card, rid)
    fields = fcard.render_row_text(st, doc=doc, question=qtext, qtype="noul" if qt == "Q3" else "choice", card=cir,
                                   options=opts, wording=card["wording_text"][wid])
    out = {"id": rid, "qtype": "noul" if qt == "Q3" else "choice", "options": opts, "gold": gold, **fields}
    must = fcard.must_show(cir, question=qtext, wording=card["wording_text"][wid])
    if qt != "Q3":
        must += [t for r, g, t in stmts if g == "policy"]
    res = fcard.loader_check(out, must_show=must)
    if not res["ok"]:
        raise EM.GateFail(f"loader {res['problems'][:2]}")
    plen = EM.prompt_len(out)
    if plen >= EM.LEN_CAP:
        raise EM.GateFail("length")
    b = S5.gate_s5(out, vocab, row["gold"], card)
    if qt == "Q3":
        if b != out["gold"]:
            raise EM.GateFail(f"S5 solver B {b} != {out['gold']}")
    else:
        bb = card["cbd_label"] if b == card.get("cbd_label") else b
        if bb != out["gold"]:
            raise EM.GateFail(f"S5 solver B {b} != {out['gold']}")
    from canon import structure_hash
    shash = structure_hash(*EM.to_display_struct(card, S, row["cases"], row["q"]))
    return row, out, st, wid, plen, shash


def gen_dev(args):
    kind, card, pack, target, level = args
    import emit as EM
    import parse_f1 as PF
    import rows as R
    import solver_a as A
    from fmt1 import card as fcard
    from fmt1.render import FormatError
    from render_f1 import RenderFail
    t0 = time.time()
    vocab = PF.vocab_for(pack)
    gb = R.GroupBuilder(card, pack, R.Trackers(), f"dev|{kind}|{card['card_id']}|{level}", held_out=True)
    out, side, stats, fails = [], [], Counter(), []
    tries = 0
    while len(out) < target and tries < target * 40:
        tries += 1
        rid = f"F1r1d-{kind}-{card['card_id']}-{level or 0}-{tries:04d}"
        try:
            if kind == "s5":
                row, j, st, wid, plen, shash = s5_row(card, pack, gb, rid, vocab)
                sampler = "S5"
            else:
                deep = level >= 5
                gb.target_depth = level
                gb.deep_tries = int(os.environ.get("F1_DEEP_TRIES", "150"))
                row = gb.build_q3(deep=deep) if card["qtype"] == "Q3" else gb.build_q1(deep=deep)
                if row["depth"] != level:
                    stats["depth_miss"] += 1
                    continue
                fields, must, st, wid, opts, gold, canon_opts, qtext = EM.render_row(card, pack, row, rid,
                                                                                     held_out=True)
                j = {"id": rid, "qtype": "noul" if row["q"]["qtype"] == "Q3" else "choice", "options": opts,
                     "gold": gold, **fields}
                res = fcard.loader_check(j, must_show=must)
                if not res["ok"]:
                    raise EM.GateFail(f"loader {res['problems'][:2]}")
                plen = EM.prompt_len(j)
                if plen >= EM.LEN_CAP:
                    raise EM.GateFail("length")
                shash, parsed = EM.gate_row(card, pack, row, j, vocab, canon_opts)
                sampler = card.get("sweep_sampler", "S1")
        except A.Reject:
            stats["reject"] += 1
            continue
        except (EM.GateFail, RenderFail, FormatError, KeyError, ValueError, PF.ParseError) as e:
            stats["fail:" + str(e)[:40]] += 1
            if "length" not in str(e):
                fails.append((rid, str(e)[:300]))
            continue
        rowj = _row_json({**card, "sampler": sampler}, row, rid, rid, rid, j, j["options"], j["gold"], st, wid,
                         shash, plen, "base", None, True, "dev")
        rowj["meta"]["dev_part"] = "S5" if kind == "s5" else "depth_sweep"
        if kind != "s5":
            rowj["meta"]["sweep_level"] = level
        out.append(rowj)
        gb.account_row(row)   # r1.1: dev rows were never booked, so every Q3 dev card had one answer only
        side.append(_sidecar(card, row, rid, rid, plen, None, None))
    return {"kind": kind, "card_id": card["card_id"], "level": level, "rows": out, "side": side,
            "stats": dict(stats), "fails": fails[:20], "secs": round(time.time() - t0, 1)}


def run_dev(n_proc=8):
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    dev = [c for c in D["dev"] if c["qtype"] in ("Q1", "Q3")]
    s5_cards = dev[: len(dev) // 2]
    sw_cards = dev[len(dev) // 2:]
    jobs = []
    per = -(-400 // len(s5_cards))
    from cards import card_statements
    for c in s5_cards:
        cc = dict(c)
        cc["constructs"] = {x for x in c["constructs"] if x not in ("last", "inert")}
        cc["fit_tokens"] = 1700          # small structures: the flowchart compiles every literal
        jobs.append(("s5", cc, allp[c["pack_id"]], per, None))
    for level in (2, 3, 4, 5, 6):
        per_l = -(-60 // len(sw_cards))
        for i, c in enumerate(sw_cards):
            cc = dict(c)
            cc["sampler"] = "S1" if i % 2 == 0 else "S2"
            cc["sweep_sampler"] = cc["sampler"]
            cc["qtype"], cc["world"], cc["defs"], cc["illus"] = "Q3", "closed", "one_line", {}
            cc["short"] = False
            cc["yes_rate"] = 0.5
            base = {x for x in c["constructs"] if x.startswith(("num_", "cat_", "bool_", "date_"))}
            cc["constructs"] = base | {"exc", "exc2", "notices", "replace", "insert", "repeal", "onlyif"}
            if cc["fallback"] is None:
                others = [o for o in cc["outcomes"] if o not in (cc["escalate"], cc["default"], cc["M"])]
                if not others:
                    continue
                cc["fallback"] = others[0]
                cc["roles"] = {**cc["roles"], others[0]: "fallback"}
            cc["listed_keys"], cc["listed_names"] = [], []
            cc["_stmts"] = card_statements(cc)
            cc["fit_tokens"] = 1100 if level >= 5 else 1250
            jobs.append(("sweep", cc, allp[c["pack_id"]], per_l, level))
    progress(f"dev: start {len(jobs)} jobs (S5 {len(s5_cards)} cards, sweep {len(sw_cards)} cards x 5 levels)")
    res_all = []
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(gen_dev, jobs):
            res_all.append(res)
            log(f"[dev] {res['kind']} {res['card_id']} L{res['level']} rows {len(res['rows'])} {res['stats']} "
                f"fails {res['fails'][:2]}")
    with open(TMP / "dev_results.pkl", "wb") as f:
        pickle.dump(res_all, f)
    s5 = [r for x in res_all if x["kind"] == "s5" for r in x["rows"]]
    sw = defaultdict(list)
    for x in res_all:
        if x["kind"] == "sweep":
            sw[x["level"]] += x["rows"]
    progress(f"dev: S5 {len(s5)} items, sweep " + ", ".join(f"L{k} {len(v)}" for k, v in sorted(sw.items())))
    return res_all


if __name__ == "__main__" and sys.argv[1] == "dev":
    run_dev(int(sys.argv[2]) if len(sys.argv) > 2 else 8)


# ---------------------------------------------------------------- G4

def g4_s5(args):
    """S5 G4 on extra draws (tested and discarded): M1, M2, M5, M8, M9, M10."""
    card, pack, n = args
    import emit as EM
    import parse_f1 as PF
    import rows as R
    import s5 as S5
    import solver_a as A
    import solver_b as SB
    vocab = PF.vocab_for(pack)
    gb = R.GroupBuilder(card, pack, R.Trackers(), f"g4s5|{card['card_id']}", held_out=True)
    res = Counter()
    fails = []
    done = 0
    t0 = time.time()
    while done < n and time.time() - t0 < 1200:
        rid = f"g4s5-{card['card_id']}-{done}"
        try:
            row, out, st, wid, plen, shash = s5_row(card, pack, gb, rid, vocab)
        except Exception:
            continue
        done += 1
        # M1: option shuffle (loader map-back under two random orders)
        from fmt1 import card as fcard
        nn = 2 if out["qtype"] == "noul" else len(out["options"])
        okm1 = True
        rng = random.Random(rid)
        for t in range(2):
            p = list(range(nn))
            rng.shuffle(p)
            okm1 = okm1 and fcard.loader_check(out, perm=p, check_rows=False)["ok"]
        res["M1:" + ("pass" if okm1 else "fail")] += 1
        # M2: outcome rename (bijection) -> re-render and walk the parsed flowchart
        try:
            outs = list(card["outcomes"])
            perm = outs[:]
            random.Random(rid + "m2").shuffle(perm)
            c2 = dict(card)
            c2["display"] = {o: card["display"][q] for o, q in zip(outs, perm)}
            gb2 = R.GroupBuilder(c2, pack, R.Trackers(), f"g4s5m2|{rid}", held_out=True)
            import copy
            S = row["S"]
            from render_f1 import Fmt, question
            stmts = S5.s5_statements(c2, S)
            fm = Fmt(c2, S)
            doc = S5.s5_doc(c2, S, row["cases"][0], fm, random.Random(1), stmts)
            qtext = question(c2, row["q"], random.Random(1))
            opts, gold, canon = EM.options_and_gold(c2, row)
            # the renamed item is rendered exactly as s5_row renders items (same card IR, built from c2)
            ents = [{"name": c2["display"][o], "text": card["meanings"][o]} for o in card["outcomes"]]
            if out["qtype"] == "noul":
                cir2 = {"title": None, "blocks": [{"type": "items", "items": [t for r, g, t in stmts]},
                                                  {"type": "defs", "variant": "DV01", "heading": None,
                                                   "entries": ents}]}
            else:
                cir2 = {"title": None, "blocks": [{"type": "items",
                                                   "items": [t for r, g, t in stmts if g == "answer"]},
                                                  {"type": "defs", "variant": "DV01", "heading": None,
                                                   "entries": ents}]}
            f2 = fcard.render_row_text(st, doc=doc, question=qtext, qtype=out["qtype"], card=cir2, options=opts,
                                       wording=card["wording_text"][wid])
            o2 = {"id": rid + "m2", "qtype": out["qtype"], "options": opts, "gold": gold, **f2}
            b = S5.gate_s5(o2, vocab, row["gold"], c2)
            want = gold if out["qtype"] != "noul" else out["gold"]
            if out["qtype"] != "noul" and b == card.get("cbd_label"):
                b = card["cbd_label"]
            res["M2:" + ("pass" if b == want else "fail")] += 1
        except Exception as e:  # noqa: BLE001
            res["M2:fail"] += 1
            fails.append(("M2", rid, str(e)[:120]))
        # M5: distractor date change -> gold unchanged (solver A)
        S = row["S"]
        case = row["cases"][0]
        ds = [k for k, a in S.attrs.items() if a.role == "distractor"]
        if ds:
            c2 = case.copy(vals=dict(case.vals))
            c2.vals[ds[0]] = S.attrs[ds[0]].lo + 3
            r2 = A.solve(S, c2)
            res["M5:" + ("pass" if r2["final"] == row["res"]["final"] else "fail")] += 1
        # M8: closed world, add a true unreferenced Boolean fact
        if S.policy.world == "closed":
            used = {m.attr for m in A.all_lits(S)}
            free = [k for k, a in S.attrs.items() if a.type == "bool" and k not in used and not a.presup]
            if free:
                c2 = case.copy(vals=dict(case.vals))
                c2.vals[free[0]] = True
                r2 = A.solve(S, c2)
                res["M8:" + ("pass" if r2["final"] == row["res"]["final"] else "fail")] += 1
        # M9: open world determinacy agrees with the flowchart walk over completions (checked inside gate_s5)
        if S.policy.world == "open" and case.unknown:
            res["M9:pass"] += 1
        # M10: negation flips the yes/no answer; double negation equals the affirmative
        if row["q"]["qtype"] == "Q3":
            X = row["q"]["X"]
            a = A.q3_answer(row["res"], X, "aff")
            ok = (A.q3_answer(row["res"], X, "neg") == 1 - a and A.q3_answer(row["res"], X, "dneg") == a)
            res["M10:" + ("pass" if ok else "fail")] += 1
    res["rows"] = done
    return {"card_id": card["card_id"], "sampler": "S5", "res": dict(res), "fails": fails[:20]}


def run_g4(n_proc=8, per_sampler=1000):
    import mr
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    jobs = []
    by_s = defaultdict(list)
    for c in D["cards"]:
        by_s[c["sampler"]].append(c)
    for smp, cs in by_s.items():
        per = -(-per_sampler // len(cs)) + 1
        for c in cs:
            jobs.append(("tr", (c, allp[c["pack_id"]], per)))
    dev = [c for c in D["dev"] if c["qtype"] in ("Q1", "Q3")]
    s5_cards = dev[: len(dev) // 2]
    per5 = -(-1000 // len(s5_cards)) + 2
    for c in s5_cards:
        cc = dict(c)
        cc["constructs"] = {x for x in c["constructs"] if x not in ("last", "inert")}
        jobs.append(("s5", (cc, allp[c["pack_id"]], per5)))
    progress(f"G4: start {len(jobs)} jobs ({per_sampler}+ base rows per training sampler; S5 >= 1000 extra draws)")
    out = []

    def runner(job):
        return job
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(_g4_job, jobs):
            out.append(res)
            log(f"[g4] {res['sampler']} {res['card_id']} {res['res']} fails {res['fails'][:3]}")
    with open(TMP / "g4_results.pkl", "wb") as f:
        pickle.dump(out, f)
    agg = defaultdict(Counter)
    for r in out:
        agg[r["sampler"]].update(r["res"])
        agg[r["sampler"]]["inert_dropped"] += r.get("inert_dropped", 0)
    json.dump({k: dict(v) for k, v in agg.items()}, open(TMP / "g4_summary.json", "w"), indent=1)
    progress("G4: " + "; ".join(f"{k} rows {v['rows']} fails {sum(x for kk, x in v.items() if kk.endswith(':fail'))}"
                                 for k, v in sorted(agg.items())))
    return agg


def _g4_job(job):
    kind, args = job
    if kind == "tr":
        import mr
        return mr.run_card(args)
    return g4_s5(args)


if __name__ == "__main__" and sys.argv[1] == "g4":
    print(dict(run_g4(int(sys.argv[2]) if len(sys.argv) > 2 else 8)))


def run_topup(n_proc=9, max_per_card=150):
    """Fill the candidate shortfall: cards that fell short of their row target hand the deficit to productive cards of
    the same sampler and question type (row cap per card kept: <= 150 generated, i.e. <= 128 kept after selection)."""
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    cards = {c["card_id"]: c for c in D["cards"]}
    got = {}
    for p in (TMP / "shards_cand").glob("*.json"):
        r = json.load(open(p))
        got[r["card_id"]] = (len(r["rows"]), r["secs"])
    deficit = defaultdict(int)
    for cid, c in cards.items():
        n = got.get(cid, (0, 0))[0]
        if n < c["n_rows"]:
            deficit[(c["sampler"], c["qtype"])] += c["n_rows"] - n
    jobs = []
    for (smp, qt), d in deficit.items():
        pool = [c for c in cards.values() if c["sampler"] == smp and c["qtype"] == qt
                and got.get(c["card_id"], (0, 0))[0] >= c["n_rows"]]
        if not pool:
            pool = [c for c in cards.values() if c["sampler"] == smp and got.get(c["card_id"], (0, 0))[0] >= c["n_rows"]]
        pool.sort(key=lambda c: got.get(c["card_id"], (0, 9e9))[1] / max(1, got.get(c["card_id"], (1, 0))[0]))
        if not pool:
            continue
        per = -(-d // len(pool))
        for c in pool:
            room = max_per_card - got[c["card_id"]][0]
            t = min(per, room)
            if t > 0 and d > 0:
                jobs.append((c, allp[c["pack_id"]], min(t, d), "topup", False))
                d -= t
    shard_dir = TMP / "shards_topup"
    shard_dir.mkdir(parents=True, exist_ok=True)
    progress(f"rows[topup]: {len(jobs)} cards, deficit {sum(deficit.values())} rows "
             f"({dict((f'{k[0]}/{k[1]}', v) for k, v in deficit.items())})")
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(gen_card, jobs):
            with open(shard_dir / f"{res['card_id']}.json", "w") as f:
                json.dump(res, f, ensure_ascii=False)
            log(f"[topup] {res['card_id']} rows {len(res['rows'])} secs {res['secs']} stats {res['stats']}")
    return deficit


if __name__ == "__main__" and sys.argv[1] == "topup":
    print(run_topup(int(sys.argv[2]) if len(sys.argv) > 2 else 9))


def run_sweep_extra(n_proc=9):
    """Extra depth-sweep items for the levels that fell short of 60 (more chain moves, leaner structures)."""
    res_all = pickle.load(open(TMP / "dev_results.pkl", "rb"))
    have = Counter()
    for x in res_all:
        if x["kind"] == "sweep":
            have[x["level"]] += len(x["rows"])
    D = _load_cards()
    from packs_f1 import load_all
    from cards import card_statements
    allp = load_all()
    dev = [c for c in D["dev"] if c["qtype"] in ("Q1", "Q3")]
    sw_cards = dev[len(dev) // 2:]
    jobs = []
    for level in (5, 6):
        need = 60 - have[level]
        if need <= 0:
            continue
        per = -(-need // len(sw_cards)) + 1
        for i, c in enumerate(sw_cards):
            cc = dict(c)
            cc["card_id"] = c["card_id"]
            cc["sampler"] = "S2" if i % 2 == 0 else "S1"
            cc["sweep_sampler"] = cc["sampler"]
            cc["qtype"], cc["world"], cc["defs"], cc["illus"] = "Q3", "closed", "one_line", {}
            cc["short"], cc["yes_rate"] = False, 0.5
            base = {x for x in c["constructs"] if x.startswith(("num_", "cat_", "bool_"))}
            cc["constructs"] = base | {"exc", "exc2", "notices", "insert", "repeal", "replace", "onlyif"}
            if cc["fallback"] is None:
                others = [o for o in cc["outcomes"] if o not in (cc["escalate"], cc["default"], cc["M"])]
                if not others:
                    continue
                cc["fallback"] = others[0]
                cc["roles"] = {**cc["roles"], others[0]: "fallback"}
            cc["listed_keys"], cc["listed_names"] = [], []
            cc["_stmts"] = card_statements(cc)
            cc["fit_tokens"] = 1400
            jobs.append(("sweep", cc, allp[c["pack_id"]], per, level))
    os.environ["F1_DEEP_TRIES"] = "400"
    progress(f"dev sweep extra: {len(jobs)} jobs for levels {[l for l in (5, 6) if have[l] < 60]} (have {dict(have)})")
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(gen_dev, jobs):
            res["kind"] = "sweep"
            for r in res["rows"]:
                r["id"] = r["id"].replace("F1r1d-sweep", "F1r1d-sweepx")
                r["group_id"] = r["call_id"] = r["id"]
            for sd in res["side"]:
                sd["id"] = sd["id"].replace("F1r1d-sweep", "F1r1d-sweepx")
                sd["group_id"] = sd["id"]
            res_all.append(res)
            log(f"[dev+] sweep {res['card_id']} L{res['level']} rows {len(res['rows'])} {res['stats']}")
    with open(TMP / "dev_results.pkl", "wb") as f:
        pickle.dump(res_all, f)
    have2 = Counter()
    for x in res_all:
        if x["kind"] == "sweep":
            have2[x["level"]] += len(x["rows"])
    progress(f"dev sweep extra done: sweep per level {dict(sorted(have2.items()))}")


if __name__ == "__main__" and sys.argv[1] == "sweepx":
    run_sweep_extra(int(sys.argv[2]) if len(sys.argv) > 2 else 9)


def run_g4_s5_only(n_proc=9):
    """Re-run the S5 part of G4 (>= 1,000 extra S5 draws, tested and discarded) and replace S5 in the summary."""
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    dev = [c for c in D["dev"] if c["qtype"] in ("Q1", "Q3")]
    s5_cards = dev[: len(dev) // 2]
    per5 = -(-1000 // (len(s5_cards) - 1)) + 2      # margin: >= 1,000 draws even if one slow card stops early
    jobs = []
    for c in s5_cards:
        cc = dict(c)
        cc["constructs"] = {x for x in c["constructs"] if x not in ("last", "inert")}
        jobs.append(("s5", (cc, allp[c["pack_id"]], per5)))
    progress(f"G4 S5 re-run: {len(jobs)} jobs")
    out = []
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(_g4_job, jobs):
            out.append(res)
            log(f"[g4s5] {res['sampler']} {res['card_id']} {res['res']} fails {res['fails'][:3]}")
    old = pickle.load(open(TMP / "g4_results.pkl", "rb")) if (TMP / "g4_results.pkl").exists() else []
    old = [r for r in old if r["sampler"] != "S5"] + out
    with open(TMP / "g4_results.pkl", "wb") as f:
        pickle.dump(old, f)
    agg = defaultdict(Counter)
    for r in old:
        agg[r["sampler"]].update(r["res"])
        agg[r["sampler"]]["inert_dropped"] += r.get("inert_dropped", 0)
    json.dump({k: dict(v) for k, v in agg.items()}, open(TMP / "g4_summary.json", "w"), indent=1)
    progress("G4: " + "; ".join(f"{k} rows {v['rows']} fails {sum(x for kk, x in v.items() if kk.endswith(':fail'))}"
                                 for k, v in sorted(agg.items())))
    return agg


if __name__ == "__main__" and sys.argv[1] == "g4s5":
    print(dict(run_g4_s5_only(int(sys.argv[2]) if len(sys.argv) > 2 else 9)))


def g4_results_from_log(since):
    """Rebuild g4_results.pkl for the training samplers from the full per-card result dicts that run_g4 logs (used
    when the run's parent is stopped while only an S5 job is still running; S5 is then re-run by g4s5)."""
    import ast
    out = []
    seen = set()
    for line in open(TMP / "build.log"):
        parts = line.split(" ", 4)
        if len(parts) < 5 or parts[0] < since:
            continue
        # [g4] training cards of the main run (its S5 jobs are superseded by the [g4s5] re-run); [g4+] extra rows
        if not ((parts[1] == "[g4]" and parts[2] != "S5") or parts[1] in ("[g4+]", "[g4s5]")):
            continue
        smp, cid, rest = parts[2], parts[3], parts[4]
        if cid in seen:
            continue
        d = ast.literal_eval(rest[: rest.index("} fails ") + 1])
        fails = ast.literal_eval(rest[rest.index("} fails ") + 8:].strip())
        seen.add(cid)
        out.append({"card_id": cid, "sampler": smp, "res": d, "fails": fails})
    with open(TMP / "g4_results.pkl", "wb") as f:
        pickle.dump(out, f)
    agg = defaultdict(Counter)
    for r in out:
        agg[r["sampler"]].update(r["res"])
    json.dump({k: dict(v) for k, v in agg.items()}, open(TMP / "g4_summary.json", "w"), indent=1)
    progress("G4: " + "; ".join(f"{k} rows {v['rows']} fails {sum(x for kk, x in v.items() if kk.endswith(':fail'))}"
                                 for k, v in sorted(agg.items())))
    return len(out), len(seen)


if __name__ == "__main__" and sys.argv[1] == "g4fromlog":
    print(g4_results_from_log(sys.argv[2]))


def run_g4_more(sampler, per_card, n_cards, n_proc=9):
    """Extra G4 base rows for one training sampler (new seed stream 'more'), appended to g4_results.pkl."""
    D = _load_cards()
    from packs_f1 import load_all
    allp = load_all()
    cs = [c for c in D["cards"] if c["sampler"] == sampler][:n_cards]
    jobs = [("tr", (c, allp[c["pack_id"]], per_card, "more")) for c in cs]
    out = []
    with Pool(n_proc) as pool:
        for res in pool.imap_unordered(_g4_job, jobs):
            res["card_id"] += "+more"
            out.append(res)
            log(f"[g4+] {res['sampler']} {res['card_id']} {res['res']} fails {res['fails'][:3]}")
    old = pickle.load(open(TMP / "g4_results.pkl", "rb"))
    old += out
    with open(TMP / "g4_results.pkl", "wb") as f:
        pickle.dump(old, f)
    return {r["card_id"]: r["res"].get("rows") for r in out}


if __name__ == "__main__" and sys.argv[1] == "g4more":
    print(run_g4_more(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
