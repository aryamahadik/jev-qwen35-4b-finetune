"""S1 (forward rule base + premise removal) and the shared rules-kind unit builders (single rows, T1 premise twins,
Q-DET negation triples, attack twins). S2 and S5 reuse the unit builders with their own policy shapes.
"""
from __future__ import annotations

from . import common  # noqa: F401  (sys.path for fmt1)

import random

from fmt1 import labels as flabels
from fmt1.render import FormatError

from .common import rng_for, unit
from . import rules_gen as G, rules_rows as RR, rules_card as RC, render_f6 as RF, rowmake as M, solver_a as A
from . import styles_f6 as ST
from .lex import OPTION_TEXT, FRAMES

YN_FORMS = ("qdet", "qest", "qplain")
CMP = RF.CMP_WORDS


class Skip(Exception):
    pass


# ---------------------------------------------------------------- cards

def _s2_gap_vars(P) -> int:
    """Variables of an S2 card profile that can show a gap: quantities and categories always; events and classes
    unless the world closes them (closed world, no evidence tag)."""
    n = len(P["qty"]) + len(P["cats"])
    if P["world"] != "closed" or P.get("ev_tag"):
        n += len(P["evs"]) + len(P["adjs"])
    return n


def make_card(card_id: str, sampler: str, schema: str, pack: dict, table: bool = False) -> dict:
    rng = rng_for("card", card_id)
    mode = "rich" if schema == "yn" else ("table" if table else "lean")
    P = G.make_profile(rng, pack, schema, sampler, table, mode)
    if sampler == "S2":
        # repair r1 v3e (G11 each card >= 5 wordings: F6-S2-c_out-01 kept 5 of 107 rows). An S2 design needs three
        # variables that can show a gap (witness w + case-split traps u, u2: s2.design); a closed-world card with no
        # evidence tag shows gaps only on quantities and categories, so a one-category pack gave 2 and every settled
        # unit failed. Card-level and label-free: redraw the profile (same rng stream) until it has three.
        for _ in range(20):
            if _s2_gap_vars(P) >= 3:
                break
            P = G.make_profile(rng, pack, schema, sampler, table, mode)
    P["local_cid"] = "k0"
    from .plan import PURE_TABLE
    if table and card_id in PURE_TABLE:   # repair r1 v3b: pure outcome-table card (k >= 18 rows; the table is the policy)
        P["pure_table"] = True            # its policy has no threshold, so rows 11-12 never apply (rules_card)
        # repair r1 v3c (length + settled traps; label-free, per card): no quantity (no row 20 line), the table's
        # column category plus ONE off-path category (3 values; its gaps give settled rows the open rows' gap
        # signature, G0 s6 'Gaps'), one notice (the base policy), open world (shortest world group)
        cs = sorted(pack["cat"], key=lambda c: -len(c["values"]))
        P["qty"] = []
        P["cats"] = [cs[0]]
        if len(cs) > 1:
            off = rng.choice(cs[1:])
            P["cats"].append(dict(off, values=list(off["values"])[:3]))
        P["n_notices"] = 1
        P["world"] = "open"
    P["order_gaps"] = mode == "rich" and P["n_notices"] >= 2 and rng.random() < 0.35
    yesno = schema == "yn"
    card = {"card_id": card_id, "sampler": sampler, "schema": schema, "pack": pack, "P": P, "table": table,
            "styles": ST.card_styles(sampler, card_id), "wordings": ST.card_wordings(card_id, yesno),
            "attack": rng.random() < 0.6,
            "nei": rng.choice(OPTION_TEXT["nei"]), "none": rng.choice(OPTION_TEXT["none"]),
            "nothing": rng.choice(OPTION_TEXT["nothing"]),
            "mask_scheme": f"MS{rng.randint(1, 12):02d}",
            "case_ref": rng.choice(["IVN01", "IVN03", "IVN04", "IVN07", "IVN08"])}
    if sampler == "S2":
        P["unless"] = P["onlyif"] = P["exc"] = P["sub"] = False
        P["order_gaps"] = False
        pk = card["pack"]
        who = rng.choice(pk["people"])
        card["narrative"] = f"{who} prepared this summary for the {pk['role']}."
        from . import scan as _scan
        if _scan.record_hits(card["narrative"]):
            card["narrative"] = None
    u = rng.random()
    if sampler == "S2":
        card["defs_style"] = "decision_list" if u < 0.6 else ("short" if u < 0.68 else "one_line")
        card["dl_variant"] = rng.choice(["DV31", "DV32", "DV33", "DV34"]) if card["defs_style"] == "decision_list" \
            else None
    else:
        # repair r1 (length): outcome-table cards (k 6-32) are short cards (no outcome glosses: k gloss lines would
        # pass the 1,900 cap); other cards are short at 8%, so short cards still hold about 15% of rows (G0 s1)
        card["defs_style"] = "short" if (table or u < 0.08) else "one_line"
        card["dl_variant"] = None
    from . import examples_f6 as EX
    n_ex, few = EX.card_flags(card_id, schema, card["defs_style"], sampler)
    exs, shots = EX.make(card, P["marker"], P["cmp_family"], n_ex, few) if n_ex else ([], [])
    card["examples"], card["fewshot"] = exs, shots
    if exs:
        card["defs_style"] = "one_line_examples"
    if yesno:
        card["frames"] = ["qdet", "qdet_leave", "qdet_dneg", "qest_est", "qest_det", "qplain_true"]
        if rng.random() < 0.3:
            card["frames"].append("qdet_imp")
        if rng.random() < 0.3:
            card["frames"].append("qest_show")
    else:
        card["frames"] = []
    return card


# ---------------------------------------------------------------- name maps (plain / masked / swapped; LR03-LR12)

def name_map(card: dict, R: dict, form: str, block_key: str) -> tuple[dict, str]:
    natural = dict(R["outcomes"])
    if form != "c_out":
        return natural, "plain"
    lf = flabels.label_form("F6", card["card_id"], block_key, rates={"masked": 0.20, "swapped": 1 / 12})
    oids = sorted(natural)
    if lf == "masked":
        ids = flabels.masked_ids(card["mask_scheme"], len(oids), f"{card['card_id']}:{block_key}")
        return dict(zip(oids, ids)), "masked"
    if lf == "swapped" and len(oids) >= 2:
        sw = flabels.swapped_names("perm", len(oids), f"{card['card_id']}:{block_key}",
                                   natural_names=[natural[o] for o in oids])
        return dict(zip(oids, sw)), "swapped"
    return natural, "plain"


# ---------------------------------------------------------------- one rules-kind row record

def gold_for(form: str, frame: str | None, T: set | None, P: set, claim) -> object:
    if form == "qdet":
        settled = len(T) == 1
        if frame in ("qdet_leave", "qdet_imp"):
            return 0 if settled else 1
        return 1 if settled else 0
    if form == "qest":
        return 1 if T == {True} else 0
    if form == "qplain":
        if len(T) != 1:
            raise Skip("qplain needs a settled claim")
        return 1 if T == {True} else 0
    raise ValueError(form)


def _flip(v):
    return {"good": "bad", "bad": "good"}.get(v)


def pick_claim(rng, R, Pset, want: str, card=None, neg_ok=True, vtarget=None):
    """A claim 'the outcome for <case> is (not) O' with T as wanted: 'true', 'false' or 'open'. Repair r1: the
    claim's valence ('yes = bad outcome', s6 / XF04: the claimed outcome's tag, flipped by 'not') is drawn per row by
    a label-free coin (vtarget), so it is balanced inside each label; outcomes with no polarity are not claimed."""
    from .emit import outcome_valence
    cat = RR.catalog(R)
    cands = []
    if want == "open":
        if len(Pset) < 2:
            return None
        cands = [(o, ng) for o in sorted(Pset) for ng in (False, True)]
    else:
        for ng in (False, True):
            pos_true = (want == "true") != ng
            if pos_true:
                if len(Pset) == 1:
                    cands.append((next(iter(Pset)), ng))
            else:
                cands += [(o, ng) for o in cat if o not in Pset]
    if not neg_ok:
        cands = [c for c in cands if not c[1]]

    def val(c):
        v = outcome_valence(card, R["outcomes"][c[0]]) if card else None
        return _flip(v) if c[1] else v
    pool = [c for c in cands if val(c) is not None]
    if vtarget:
        pool = [c for c in pool if val(c) == vtarget]
    if not pool:
        return None
    neg_coin = neg_ok and rng.random() < 0.25
    sub = [c for c in pool if c[1] == neg_coin] or pool
    o, ng = rng.choice(sub)
    return {"t": "out_is", "o": o, "neg": ng}


def claim_T(R, case, claim):
    return A.solve_rules(R, case, claim)


def display_for(rng, k: int):
    """s6 display rule: (nei_shown, none_shown) for k (k includes the abstain slots)."""
    if k == 2:
        return False, False
    nei_p, none_p = min(1.0, 0.1 * k), min(1.0, 0.05 * k)
    if k <= 4:
        u = rng.random()
        if u < nei_p:
            return True, False
        if u < nei_p + none_p:
            return False, True
        return False, False
    return rng.random() < nei_p, rng.random() < none_p


def gold_slot(rng, k: int, nei: bool, none: bool, weight_abstain: float = 2.0) -> str:
    slots = ["concrete"] * (k - nei - none) + (["nei"] if nei else []) + (["none"] if none else [])
    w = [1.0 if s == "concrete" else weight_abstain for s in slots]
    return rng.choices(slots, weights=w)[0]


def _mentions(R, x) -> int:
    """How often outcome x is named in the row's card text: rule heads / table cells naming it, plus the default."""
    return sum(1 for r in A.all_rules(R) if r["out"] == x) + (1 if x == R["default"] else 0)


def _matched(rng, R, rest: list, anchor, n: int) -> list:
    """Repair r1 v3 (G6 c, F6-QC-13): distractors matched to the anchor option's mention count in the card (rule
    heads + default), so 'the option the rules name most often' never points to the gold. Closest counts first, ties
    broken at random; label-free for the reader (every displayed concrete option has the anchor's count where the
    catalog allows it)."""
    ma = _mentions(R, anchor)
    keyed = sorted(rest, key=lambda x: (abs(_mentions(R, x) - ma), rng.random()))
    return keyed[:n]


def options_for(rng, R, Pset, gcls: str, k: int, nei_t, none_t):
    cat = RR.catalog(R)
    n_conc = k - (nei_t is not None) - (none_t is not None)
    if gcls == "concrete":
        if len(Pset) != 1:
            return None
        o = next(iter(Pset))
        rest = [x for x in cat if x != o]
        if len(rest) < n_conc - 1:
            return None
        L = [o] + _matched(rng, R, rest, o, n_conc - 1)
    elif gcls == "nei":
        if len(Pset) < 2:
            return None
        p = rng.choice(sorted(Pset))
        rest = [x for x in cat if x != p]
        if len(rest) < n_conc - 1:
            return None
        L = [p] + _matched(rng, R, rest, p, n_conc - 1)
    else:
        rest = [x for x in cat if x not in Pset]
        if len(rest) < n_conc:
            return None
        L = rng.sample(rest, n_conc)
    rng.shuffle(L)
    return L


def build_rules_unit(card: dict, spec: dict, uid: str, shape=None) -> list[dict]:
    """A unit for a rules-kind card: a list of row records (1 row, or a twin pair, triple or attack pair)."""
    rng = rng_for("unit", uid)
    P, pack = card["P"], card["pack"]
    form = spec["form"]
    case = f"{P['prefix']}-{rng.randint(1000, 9999)}"
    dis = []
    while len(dis) < 4:
        x = f"{P['prefix']}-{rng.randint(1000, 9999)}"
        if x != case and x not in dis:
            dis.append(x)
    if form == "c_case":
        from . import s2
        try:
            recs = s2.build_case_unit(rng, card, spec, uid)
        except (RR.Reject, A.Drop, FormatError, ValueError) as e:
            raise Skip(f"unit {uid} failed: {type(e).__name__}: {str(e)[:120]}")
        if spec.get("twin") == "attack":
            recs = _attack(rng, card, recs[0])
        return recs
    for attempt in range(8):
        try:
            return _try_unit(rng, card, spec, uid, form, case, dis, shape)
        except (Skip, RR.Reject, A.Drop, FormatError, ValueError) as e:
            last = e
            continue
    raise Skip(f"unit {uid} failed: {type(last).__name__}: {str(last)[:120]}")


def _policy_size(spec, card, rng):
    form = spec["form"]
    s2 = card["sampler"] == "S2"
    if form == "c_out":
        k = spec["k"]
        n_conc = k - spec["nei"] - spec["none"]
        if card["table"]:
            return (0 if k >= 18 else 1), n_conc + 4
        if s2:                     # S2 catalog = rules - 1 (r1-r4 give X, Y and the default; distractors one each);
            g = spec.get("gold")   # the catalog needs n_conc outcomes (+ |P| more for a None-gold row)
            extra = 0 if g in ("concrete", "nei") else (1 if spec.get("role") == "settled" else 2)
            # repair r1 v3d: the v3c trap rules take two catalog outcomes of their own (besides X, Y and the
            # default), so the catalog holds >= 5 outcomes; before, every S2 C-OUT draw at k 2-4 with an abstain slot
            # (and card F6-S2-c_out-01) failed 'S2 trap outcomes' (G10 NEI display at k 3, G11 cards_ge_80)
            return n_conc + 1 + extra, max(5, n_conc + 1 + extra)
        return max(2, min(9, n_conc + 1)), n_conc + 2
    if form == "c_gap":
        return rng.randint(2, 3), 3
    if s2:
        return rng.randint(4, 6), 5
    return rng.randint(3, 5), 4


def _table_shape(rng, card, spec):
    if not card["table"]:
        return None
    k = spec["k"]
    n_conc = k - spec["nei"] - spec["none"]
    need = n_conc + 1              # every displayed concrete option is a cell or the default (s6 reachable options)
    pk = card["pack"]
    maxr = min(6, len(pk["places"]))
    maxc = min(5, max(len(c["values"]) for c in card["P"]["cats"]))
    for r in range(2, maxr + 1):
        for c in range(2, maxc + 1):
            if r * c >= need:
                return (r, c)
    return (maxr, maxc)


def _try_unit(rng, card, spec, uid, form, case, dis, shape):
    P, pack = card["P"], card["pack"]
    n_rules, n_out = _policy_size(spec, card, rng)
    tshape = _table_shape(rng, card, spec)
    n_gaps = spec["n_gaps"]
    sig = spec.get("sig")
    if form in YN_FORMS:
        want = spec["want"]           # 'true' | 'false' | 'open'
        if want == "open":
            target = "open"
        elif want == "false" and form != "qplain":
            target = rng.choice(["settled", "settled", "open"])
        else:
            target = "settled" if rng.random() < 0.8 else "open"
    elif form == "c_out":
        target = {"concrete": "settled", "nei": "open"}.get(spec["gold"]) or spec.get("role", "settled")
    elif form == "c_gap":
        target = "settled" if spec["gold"] == "nothing" else "open"
    else:
        raise ValueError(form)
    if shape:
        R, asg, hidden, Pset, _, gaps = shape(rng, card, spec, case, dis, target, n_gaps, n_rules, n_out, sig=sig)
    else:
        R, asg, hidden, Pset, _, gaps = RR.build_rules_record(
            rng, P, pack, case, dis, target=target, n_gaps=n_gaps, n_rules=n_rules, n_out_min=n_out,
            table_shape=tshape, sig=sig)
    rec = {"R": R, "case": case, "asg": asg, "hidden": hidden, "P": Pset, "gaps": gaps, "form": form,
           "spec": spec, "uid": uid}
    if form in YN_FORMS:
        vt = "bad" if unit("valence", spec["sid"]) < 0.5 else "good"
        claim = pick_claim(rng, R, Pset, spec["want"], card=card, neg_ok=spec.get("twin") != "triple", vtarget=vt)
        if claim is None:
            raise Skip("no claim")
        T = claim_T(R, case, claim)
        if spec["want"] == "open" and len(T) != 2:
            raise Skip("claim not open")
        if spec["want"] in ("true", "false") and T != {spec["want"] == "true"}:
            raise Skip("claim value")
        if len(T) == 2:
            dec = A.decisive_gaps(R, case, claim)
            if len([d for d in dec if d in [g for g, _ in gaps]]) != 1:
                raise Skip("claim decisive")
        rec.update(claim=claim, T=T, frame=spec["frame"])
        rec["gold"] = gold_for(form, spec["frame"], T, Pset, claim)
        if rec["gold"] != spec["label"]:
            raise Skip("label")
    elif form == "c_out":
        L = options_for(rng, R, Pset, spec["gold"], spec["k"], card["nei"] if spec["nei"] else None,
                        card["none"] if spec["none"] else None)
        if L is None:
            raise Skip("options")
        rec.update(L=L)
    elif form == "c_gap":
        gl = [g for g, _ in gaps]
        st = A.settling_set(R, case, gl)
        if spec["gold"] == "nothing":
            if len(Pset) != 1:
                raise Skip("c_gap settled")
        elif len(st) != 1:
            raise Skip("c_gap settling set")
        elif not spec.get("cgap_balance_off"):
            from .cgap_balance import weight     # repair r1 v3d: decisive-gap balance (G10 longest option, G7)
            if rng.random() >= weight(card["card_id"], spec["k"], R, st[0]):
                raise Skip("c_gap balance")
        rec.update(settle=st)
    rec["depth"] = G.depth_of(R, case)
    rows = [rec]
    tw = spec.get("twin")
    if tw == "premise":
        from .common import premise_set
        rows = premise_set(_premise_twin, rng, card, rec)
    elif tw == "triple":
        rows = _triple(rng, card, rec)
    elif tw == "attack":
        rows = _attack(rng, card, rec)
    return rows


def _fill(R, case, var, value, allow_false_fact=False):
    """The record with one visible gap filled by a value (the settled twin; M5/M6 fills). allow_false_fact writes a
    structure-level 'known false' yes/no fact (G4 only; never rendered)."""
    import copy
    R2 = copy.deepcopy(R)
    F = R2["facts"][case]
    k = var[0]
    if k in ("num", "cat"):
        F[k][var[1]] = {"v": value}
    elif k == "ev":
        if value:
            F["ev"][var[1]] = {"v": True, "date": R["D"] - 7}
        else:
            if R2["world"] != "closed":
                if not allow_false_fact:
                    return None
                F["ev"][var[1]] = {"v": False}
            else:
                F["ev"].pop(var[1], None)
    elif k == "cls":
        lst = [(w, s) for w, s in R2["lists"][var[1]] if w != case]
        if value:
            F["cls"][var[1]] = {"v": True}
            lst = lst + [(case, "v")]
        else:
            closes = R2["world"] == "closed" or (R2["world"] == "local" and R2.get("local") == var[1])
            if not closes:
                if not allow_false_fact:
                    return None
                F["cls"][var[1]] = {"v": False}
            else:
                F["cls"].pop(var[1], None)
        R2["lists"][var[1]] = lst
    elif k == "nd":
        R2["notices"][var[1]]["date"] = {"k": "exact", "d": value}
    return R2


def _hide_fact(R, case, k, mode, asg):
    """The record with one more fact of the case hidden (a trap gap for the matched twin): marker / absent / tag /
    plan, as rules_gen.realise renders them."""
    import copy
    R2 = copy.deepcopy(R)
    F = R2["facts"][case]
    t, x = k
    if t in ("num", "cat"):
        slot = F[t]
        if mode == "absent":
            slot.pop(x, None)
        elif mode == "marker":
            slot[x] = {"m": True}
        elif mode == "tag":
            v = (slot.get(x) or {}).get("v", asg.get(k))
            if v is None:
                return None
            slot[x] = {"v": v, "tag": True}
        else:
            return None
    elif t == "ev":
        cur = F["ev"].get(x)
        if mode == "absent":
            F["ev"].pop(x, None)
        elif mode == "marker":
            F["ev"][x] = {"m": True}
        elif mode == "tag":
            if not (cur and cur.get("v") is True and "date" in cur):
                return None
            F["ev"][x] = {**cur, "tag": True}
        elif mode == "plan":
            F["ev"][x] = {"plan": R["D"] + 9}
        else:
            return None
    elif t == "cls":
        if x not in R2["lists"]:
            return None
        lst = [(w, s) for w, s in R2["lists"][x] if w != case]
        if mode == "absent":
            F["cls"].pop(x, None)
        elif mode == "marker":
            F["cls"][x] = {"m": True}
            lst.append((case, "m"))
        elif mode == "tag":
            if not (F["cls"].get(x) or {}).get("v"):
                return None
            F["cls"][x] = {"v": True, "tag": True}
            lst.append((case, "tag"))
        else:
            return None
        R2["lists"][x] = lst
    else:
        return None
    return R2


def _add_trap(rng, card, R2, case, rec, elem, check):
    """Add one trap gap with signature element `elem` to the filled twin record R2 such that check(R3) holds (the
    twin keeps the open row's n_gaps, kinds and positions: s2 'trap arm', s6 'Gaps'; F6-QC-1)."""
    roles = G.ref_vars(R2)
    rich = card["P"].get("mode") == "rich"
    asg = rec.get("asg") or {}
    shown = set(g for g, _ in G.visible_gaps(R2, case))
    cands = [k for k in roles if k[0] != "nd"] + [(a["kind"], aid) for aid, a in R2["attrs"].items()
                                                  if (a["kind"], aid) not in roles]
    rng.shuffle(cands)
    base_el = RR.elems(R2, case, G.visible_gaps(R2, case))
    for k in cands:
        if k in shown:
            continue
        ms = RR._modes(R2, k, asg.get(k), rich) if k in roles else ["marker"]
        ms = [m for m in ms if RR._pred_elem(R2, k, m, roles) == elem]
        rng.shuffle(ms)
        for m in ms:
            R3 = _hide_fact(R2, case, k, m, asg)
            if R3 is None:
                continue
            g3 = G.visible_gaps(R3, case)
            if sorted(base_el + [elem]) != RR.elems(R3, case, g3):
                continue
            try:
                if check(R3):
                    return R3, g3
            except (A.Drop, ValueError):
                continue
    return None


def _premise_twin(rng, card, rec):
    """T1 (2.2): the open row and its settled twin (the decisive premise restored, and one trap gap of the same
    kind and position added, so both arms carry the same gap signature: s2 trap arm, s6 'Gaps'); own call_ids, one
    group."""
    R, case = rec["R"], rec["case"]
    claim = rec.get("claim")
    form = rec["form"]
    sp = rec["spec"]
    if form in YN_FORMS:
        if len(rec["T"]) != 2:
            raise Skip("premise twin needs an open base")
    elif form in ("c_out", "c_gap") and len(rec["P"]) < 2:
        raise Skip("premise twin needs an open base")
    dec = A.decisive_gaps(R, case, claim if form in YN_FORMS else None)
    gk = [g for g, _ in rec["gaps"]]
    dec = [d for d in dec if d in gk]
    if len(dec) != 1:
        raise Skip("decisive")
    g = dec[0]
    elem = next(e for (gg, kk), e in zip(rec["gaps"], [f"{kk}@{G.gap_position(R, case, gg)}"
                                                        for gg, kk in rec["gaps"]]) if gg == g)
    regs = A.var_regions(R, case).get(g, [])
    vals = list(regs)
    tv = rec["asg"].get(g)
    if tv is not None and tv in vals:
        vals.remove(tv)
        vals.insert(0, tv)
    if sp.get("twin_more"):        # repair r1 v3f: twins 2, 3, ... of a set try the fill values in a random order, so a
        rng.shuffle(vals)          # set can reach its planned size with distinct records (v3e: 3 of 105 C-OUT 4-sets)
    for val in vals:
        R2 = _fill(R, case, g, val)
        if R2 is None:
            continue
        try:
            P2 = A.solve_rules(R2, case)
        except A.Drop:
            continue

        def ok(R3, P2=P2):
            P3 = A.solve_rules(R3, case)
            if form in YN_FORMS:
                T3 = A.solve_rules(R3, case, claim)
                if len(T3) != 1:
                    return False
                if gold_for(form, rec["frame"], T3, P3, claim) != sp.get("twin_label", 1 - rec["gold"]):
                    return False
                tw_want = sp.get("twin_want")
                if tw_want in ("true", "false") and T3 != {tw_want == "true"}:
                    return False
                return True
            if len(P3) != 1:
                return False
            if form == "c_out":
                return next(iter(P3)) in rec["L"]
            return True
        got = _add_trap(rng, card, R2, case, rec, elem, ok)
        if got is None:
            continue
        R3, g3 = got
        P3 = A.solve_rules(R3, case)
        tw = dict(rec)
        tw.update(R=R3, P=P3, gaps=g3, twin_kind="premise")
        if form in YN_FORMS:
            T3 = A.solve_rules(R3, case, claim)
            tw.update(T=T3, gold=gold_for(form, rec["frame"], T3, P3, claim))
        elif form == "c_gap":
            tw.update(settle=[])
        tw["depth"] = rec["depth"]
        return [tw, rec]
    raise Skip("premise twin")


def _triple(rng, card, rec):
    """Q-DET complement / equiv unit (M9, s6 relation units): affirmative, 'leave open whether', and the double
    negation over S' (S negated by 'not' on its one atom)."""
    if rec["form"] != "qdet" or rec["frame"] != "qdet":
        raise Skip("triple base")
    claim = rec["claim"]
    if claim.get("neg"):
        raise Skip("triple over an un-negated S")
    leave = "qdet_leave"
    c = dict(rec)
    c.update(frame=leave, gold=1 - rec["gold"], rel="complement")
    neg = {**claim, "neg": True}
    T3 = A.solve_rules(rec["R"], rec["case"], neg)
    e = dict(rec)
    e.update(frame="qdet_dneg", claim=neg, T=T3, gold=1 if len(T3) == 1 else 0, rel="equiv")
    if e["gold"] != rec["gold"]:
        raise Skip("dneg label")
    return [rec, c, e]


def _attack(rng, card, rec):
    a = dict(rec)
    from .lex import ATTACK_LINES
    a["attack"] = rng.choice(ATTACK_LINES)
    a["twin_kind"] = "attack"
    a["rel"] = "inv"
    return [rec, a]
