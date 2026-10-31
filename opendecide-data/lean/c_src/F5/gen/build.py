"""F5 builder: cards -> bases (phase 1) -> questions (phase 2) -> rendered rows + relations + sidecars (phase 3).

  python -m gen.build --set candidates   # round-1 candidate pool (training samplers S1-S4), 1.5 x 3,600 rows
  python -m gen.build --set qc           # separate G6 QC sample (>= 5,000 rows), other seed tag
  python -m gen.build --set mixdev       # S5 held-out dev items (400 = 100 bases x 4 rows; held-out packs and styles)
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import time

from . import gen, rows as R
from .common import (FAMILY, GEN_VERSION, LICENCE, OUT, SEED, SOURCE, SPEC_ID, negc, progress, rng_for, sha, text_lint,
                     uhash, write_jsonl)
from .plan import card_summary, plan_cards

V_UNFORCED_FRAME = 0.50
TOKEN_CAP = 1900


def setup_cards(cards, tag="r1"):
    for c in cards:
        gen.H_for(c).card_setup(c)
        fts = [f"FT{i:02d}" for i in range(1, 19) if i not in (10, 18)]
        c["fewshot_template"] = fts[int(uhash("ft", c["card_id"]) * len(fts))]
    from . import ruleset
    sigs, clashes, dup = ruleset.assign(cards, tag)
    for c in cards:
        c["rule_signature"] = sigs[c["card_id"]]
    setup_cards.last = {"rule_sets": len(sigs), "constant_assign_failures": clashes, "duplicate_signatures": dup}
    return cards


def gen_pair_cards(ca, cb, n, log):
    """Phase 1 for one antithetic card pair: mirrored slot plans, slot dropped from both cards when either fails."""
    rng = rng_for("f5-slots", ca["card_id"])
    sa = gen.plan_slots(ca, n, rng)
    sb = gen.mirror(sa)
    out_a, out_b = [], []
    pairs_a, pairs_b = {}, {}
    by_pair_slots = {}
    for s_a, s_b in zip(sa, sb):
        if s_a["pair"] is not None:
            by_pair_slots.setdefault(s_a["pair"], {})[s_a["role"]] = (s_a, s_b)
    for s_a, s_b in zip(sa, sb):
        built = []
        if s_a["pair"] is None:
            built = build_mirrored(ca, s_a, cb, s_b, log, "")
            if built is None:
                built = [None, None]
                for alt in (1, 2):
                    if alt == s_a["vk"]:
                        continue
                    got = build_mirrored(ca, dict(s_a, vk=alt), cb, dict(s_b, vk=alt), log, f"r{alt}")
                    if got is not None:
                        built = got
                        log["slot_vk_retry"] += 1
                        break
            if any(b is None for b in built):
                log["slot_dropped"] += 1
                continue
            out_a.append(built[0])
            out_b.append(built[1])
            continue
        for card, s, store, pairs in ((ca, s_a, out_a, pairs_a), (cb, s_b, out_b, pairs_b)):
            r = rng_for("f5-base", card["card_id"], s["i"])
            if s["pair"] is not None and s["role"] == "Bp":
                b = pairs.get(s["pair"])
                if b is not None and b.get("_pair") is not None:
                    nb = b.pop("_pair")
                    nb["slot"] = dict(s, g=nb["slot"]["g"])
                    nb["paired_with"] = b
                    b["paired_with_p"] = nb
                    built.append(nb)
                    continue
                log["pair_fail"] += 1
                try:
                    built.append(gen.build_base(card, dict(s, pair=None), r))
                except gen.SlotFail:
                    built.append(None)
                continue
            if s["pair"] is not None and s["role"] == "B":
                sp = by_pair_slots[s["pair"]]["Bp"][0 if card is ca else 1]
                try:
                    b = gen.build_base(card, s, r, pair_slot=sp)
                    pairs[s["pair"]] = b
                    built.append(b)
                except gen.SlotFail:
                    log["pair_unbuildable"] += 1
                    try:
                        built.append(gen.build_base(card, dict(s, pair=None), r))
                    except gen.SlotFail:
                        built.append(None)
                continue
            try:
                built.append(gen.build_base(card, s, r))
            except gen.SlotFail:
                built.append(None)
        if any(b is None for b in built) and s_a["pair"] is None:
            # one retry with another V size for both mirrored cards (templates stay mirrored)
            for alt in (1, 2):
                if alt == s_a["vk"]:
                    continue
                t_a, t_b = dict(s_a, vk=alt), dict(s_b, vk=alt)
                try:
                    built = [gen.build_base(ca, t_a, rng_for("f5-base-r", ca["card_id"], s_a["i"], alt)),
                             gen.build_base(cb, t_b, rng_for("f5-base-r", cb["card_id"], s_b["i"], alt))]
                    log["slot_vk_retry"] += 1
                    break
                except gen.SlotFail:
                    built = [None, None]
        if any(b is None for b in built):
            log["slot_dropped"] += 1
            for card, s, pairs in ((ca, s_a, pairs_a), (cb, s_b, pairs_b)):
                if s["pair"] is not None and s["role"] == "B":
                    pairs.pop(s["pair"], None)
            continue
        out_a.append(built[0])
        out_b.append(built[1])
    # a B whose B' failed and fell back stays unpaired; so does a B whose B' slot was dropped (repair r2: the link to
    # a B' that is not in the output is removed, so B is never counted as a contrast-set member without its twin)
    for lst in (out_a, out_b):
        ids_in = {id(x) for x in lst}
        for b in lst:
            if "paired_with_p" in b and id(b["paired_with_p"]) not in ids_in:
                del b["paired_with_p"]
                log["pair_bp_dropped"] += 1
        for b in lst:
            if b["slot"]["pair"] is not None and b["slot"]["role"] == "B" and "paired_with_p" not in b:
                b["slot"] = dict(b["slot"], pair=None)
    return out_a, out_b


def build_mirrored(ca, s_a, cb, s_b, log, tag):
    """Repair r2: an unpaired slot of card A and its mirrored slot of partner B (v -> 1 - v, g -> 1 - g) are built with
    one V template class, so each class is seen once with gold g and once with 1 - g. A class that B cannot realize
    is excluded and A is rebuilt (at most 4 classes); None when no shared class is found."""
    excl = set()
    for t in range(4):
        ka = ("f5-base", ca["card_id"], s_a["i"]) + ((tag,) if tag else ()) + ((t,) if t else ())
        kb = ("f5-base", cb["card_id"], s_b["i"]) + ((tag,) if tag else ()) + ((t,) if t else ())
        try:
            ba = gen.build_base(ca, s_a, rng_for(*ka), exclude_cls=excl)
        except gen.SlotFail:
            return None
        cls = gen.vcls(ba["cores"][ba["vcore"]])
        try:
            bb = gen.build_base(cb, s_b, rng_for(*kb), force_cls=cls, attempts=100)
        except gen.SlotFail:
            excl.add(cls)
            log["vcls_redraw"] += 1
            continue
        return [ba, bb]
    return None


def phase1(cards, bases_per_card, log):
    by_pair = collections.defaultdict(list)
    for c in cards:
        by_pair[c["pair_index"]].append(c)
    allb = []
    t0 = time.time()
    for pi in sorted(by_pair):
        ca, cb = by_pair[pi]
        n = bases_per_card(ca)
        a, b = gen_pair_cards(ca, cb, n, log)
        for lst, card in ((a, ca), (b, cb)):
            for j, base in enumerate(lst):
                base["base_id"] = f"{card['card_id']}-b{j:03d}"
                base["mk"] = f"mk{pi}-{base['slot']['i']}"     # mirror key: same for the mirrored slot of the partner
            allb += lst
        log["pairs_done"] += 1
        if log["pairs_done"] % 10 == 0:
            print(f"  phase1 {log['pairs_done']} card pairs, {len(allb)} bases, {time.time() - t0:.0f}s", flush=True)
    return allb


def frame_share(bases):
    forced = collections.Counter()
    tot = collections.Counter()
    for b in bases:
        c = b["cores"][b["vcore"]]
        s = b["card"]["sampler"]
        tot[s] += 1
        if b["vn2"] == 0 and not c.matrix:
            forced[s] += 1
    return {s: forced[s] / tot[s] + (1 - forced[s] / tot[s]) * V_UNFORCED_FRAME for s in tot}


def phase2(bases):
    """V questions first (unforced framing 0.5); the realized V framed share per sampler then sets the A / N / D framing
    probability, so the framed share per row type is equal (SEM-01, +/- 3 pp)."""
    fr = collections.defaultdict(list)
    for b in bases:
        if "paired_with" in b:
            continue
        q = gen.compose_v(b, V_UNFORCED_FRAME, rng_for("f5-q-v", b["mk"]))
        fr[b["card"]["sampler"]].append(q[-1] == "FR" or q[-1].startswith("FR|"))
    share = {k: sum(v) / len(v) for k, v in fr.items()}
    for b in bases:
        if "paired_with" in b:
            continue
        r = rng_for("f5-q", b["mk"])
        b["rows"] = gen.compose_rows(b, share[b["card"]["sampler"]], r)
    for b in bases:
        if "paired_with" in b:
            b["rows"] = b["paired_with"]["rows"]
            b["two_lcore"] = b["paired_with"].get("two_lcore", False)
    return share


def evaluate(b):
    """Gold per row by solver A on M; identities asserted (N = 1 - A, D = A, V' = V, XOR on truth-functional chains)."""
    H = gen.H_for(b["card"])
    keys = list(b["rows"])
    vals = H.solve(b["M"], [b["rows"][k][1] for k in keys])
    g = {k: int(v) for k, v in zip(keys, vals)}
    v = b["v"]
    assert g["A"] == v, (b["base_id"], "A != v(P)")
    assert g["N"] == 1 - v, (b["base_id"], "N != 1 - A")
    assert g["D"] == v, (b["base_id"], "D != A")
    for t in keys:
        q, lf, k, fams, flips, key = b["rows"][t]
        core = lf
        while core[0] == "not":
            core = core[1]
        if set(fams) <= {"C1", "C2", "C3", "C5", "C6"} and fams and core == b["P"]:
            assert g[t] == v ^ (k % 2), (b["base_id"], t, "XOR identity")
    if "Vp" in g:
        assert g["Vp"] == g["V"]
    assert g["V"] == b["slot"]["g"], (b["base_id"], "V gold != target")
    return g


def phase3(bases, *, held_out=False, set_tag="r1"):
    """Render every row through fmt1 (render_and_check = loader_check) and build meta, relations and sidecars."""
    rows_out, rels, side = [], [], []
    fails = collections.Counter()
    # G10 fix (8 Oct 2026, owner "fix those families"): spec 3.1 short card = about 15% of BASES, but inverted-card
    # bases always take the full form, so the old draw (uhash < 0.15 on non-inverted bases only) gave ~13% expected
    # (qc_sample 0.1177 < 0.12). Draw non-inverted bases at 0.15 / (1 - inverted base share) so the overall share is ~15%.
    n_inv = sum(1 for b in bases if b["card"].get("inverted"))
    p_short = min(1.0, 0.15 / max(1e-9, 1.0 - n_inv / max(1, len(bases))))
    for b in bases:
        card = b["card"]
        H = gen.H_for(card)
        gold = evaluate(b)
        b["gold"] = gold
        mkb = b["paired_with"]["mk"] if "paired_with" in b else b["mk"]   # B' takes B's draws (one pair, one cell)
        attack, push = R.attack_text(b["mk"])
        doc = H.doc(b["M"])
        doc_att = H.doc(b["M"], attack=attack) if "Vp" in b["rows"] else None
        if "styles" not in card:
            card["styles"] = R.card_styles(dict(card, card_id=f"F5-{set_tag}-pair{card['pair_index']}"),
                                           [doc] + ([doc_att] if doc_att else []), held_out=held_out)
        sts = [s for s in card["styles"] if R.can_render(doc, s) and (doc_att is None or R.can_render(doc_att, s))]
        if not sts:
            sts = R.card_styles(dict(card, card_id=card["card_id"] + "*"), [doc] + ([doc_att] if doc_att else []),
                                held_out=held_out)
        if "paired_with" in b:
            style = b["paired_with"]["style"]
            if not R.can_render(doc, style):
                fails["pair_style"] += 1
                continue
        else:
            style = sts[int(uhash("style", b["mk"]) * len(sts))]
        b["style"] = style
        # card: trigger set over every row of the base (both bases of a pair), full or short form
        trig = set(H.text_triggers(b["M"]))
        for t, (q, lf, k, fams, flips, key) in b["rows"].items():
            trig |= question_triggers(fams, q)
            if hasattr(H, "lf_triggers"):
                trig |= H.lf_triggers(lf)
        if "paired_with" in b:
            trig |= b["paired_with"]["trig"]
        elif "paired_with_p" in b:
            trig |= set(H.text_triggers(b["paired_with_p"]["M"]))
        b["trig"] = trig
        full = H.full_keys(card)
        short = uhash("short", mkb) < p_short \
            and not card.get("inverted")
        if not trig <= full:
            fails["trigger_outside_full"] += 1
            full |= trig
        keys = trig if short else full
        params = H.sem_params(card, b["M"])
        params["value_sets_full"] = [(a, v, params.get("vs_form", "case")) for a, v in params.get("value_sets", [])]
        if short:
            used_vs = set(params.get("used_value_sets", [a for a, _ in params.get("value_sets", [])]))
            params["value_sets_full"] = [x for x in params["value_sets_full"] if x[0] in used_vs]
        civ, defs_style, dv = R.card_ir(card, keys, params, short=short,
                                         fewshot_examples=H.fewshot(card, b) if card.get("fewshot") else None,
                                         inverted_block=H.inverted_block(card, b) if card.get("inverted") else None)
        b["card_ir"], b["card_keys"], b["defs_style"], b["dv"] = civ, sorted(keys), defs_style, dv
        wl = card["wordings"]
        w = wl[int(uhash("wording", mkb) * len(wl))]
        b["wording"] = w
        ids = {t: f"f5{set_tag}-{sha(b['base_id'] + '|' + t)[:12]}-{t}" for t in b["rows"]}
        b["ids"] = ids
        for t, (q, lf, k, fams, flips, key) in b["rows"].items():
            d = doc_att if t == "Vp" else doc
            try:
                fields, res = R.render_row(style, d, q, w["text"], gold[t], civ, ids[t])
            except Exception as e:  # noqa: BLE001
                fails["render:" + type(e).__name__] += 1
                fails["last"] = str(e)[:200]
                break
            row = make_row(b, t, ids, fields, gold[t], style, w, defs_style, held_out)
            row["_base"] = b["base_id"]
            rows_out.append(row)
            side.append(side_record(b, t, row, q, k, fams, flips, key, push if t == "Vp" else None))
        else:
            continue
    # length cap (G0 section 1): every row < 1,900 real tokens on the served prompt (instructions twice); a base
    # with a longer row is skipped, never cut, and so is its contrast-pair partner
    from .gates import served_tokens
    over = set()
    for r in rows_out:
        if served_tokens(r) >= TOKEN_CAP:
            over.add(r["_base"])
    by_slot = {(b["card"]["card_id"], b["slot"]["i"]): b for b in bases}
    for _ in range(2):   # the contrast-pair partner and the antithetic partner card's mirrored slot go too
        for b in bases:
            if b["base_id"] in over:
                for x in (b.get("paired_with"), b.get("paired_with_p"),
                          by_slot.get((b["card"]["partner"]["card_id"], b["slot"]["i"]))):
                    if x is not None:
                        over.add(x["base_id"])
    fails["length_cap_bases"] = len(over)
    rows_out = [r for r in rows_out if r["_base"] not in over]
    keep_ids = {r["id"] for r in rows_out}
    side = [x for x in side if x["id"] in keep_ids]
    for r in rows_out:
        r["_bid"] = r.pop("_base", None)
    for b in bases:
        if b["base_id"] in over:
            b.pop("ids", None)
    for b in bases:
        if "ids" not in b:
            continue
        ids = b["ids"]
        rels.append({"a": ids["A"], "b": ids["N"], "type": "complement"})
        rels.append({"a": ids["A"], "b": ids["D"], "type": "equiv"})
        if "Vp" in ids:
            rels.append({"a": ids["V"], "b": ids["Vp"], "type": "inv"})
    return rows_out, rels, side, fails


QFAM_KEYS = {"C13": {"SEM-10"}, "C16": {"SEM-28"}, "C12": {"SEM-24"}, "C9": {"SEM-08", "SEM-12", "SEM-14"},
             "C5": {"SEM-19"}, "C3": {"SEM-19", "SEM-27"}, "C8": {"SEM-22"}, "C11": {"SEM-23"},
             "C14": {"SEM-25"}, "C15": {"SEM-26", "SEM-27"}, "C10": {"SEM-11"}, "C7": {"SEM-20"},
             "C6": {"SEM-18"}}


def question_triggers(fams, q):
    keys = {"SEM-01"}
    for f in fams:
        keys |= QFAM_KEYS.get(f, set())
    return keys


def make_row(b, t, ids, fields, gold, style, w, defs_style, held_out):
    card = b["card"]
    rtype = {"A": "aff", "N": "neg", "D": "dneg", "V": "var", "Vp": "attack"}[t]
    if t in ("N", "D", "V"):
        twin_of, twin_kind = ids["A"], "negation"
    elif t == "Vp":
        twin_of, twin_kind = ids["V"], "attack"
    elif "paired_with" in b:
        twin_of, twin_kind = b["paired_with"]["ids"]["A"], "fact_flip"
    else:
        twin_of, twin_kind = None, None
    pair_root = b["paired_with"]["base_id"] if "paired_with" in b else b["base_id"]
    q, lf, k, fams, flips, key = b["rows"][t]
    deep = (k == 3) or b["info"]["depth"] >= 3
    unit = "u2" if t in ("V", "Vp") else "u1"
    meta = {"family": FAMILY, "spec_id": SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack"]["pid"],
            "sampler": card["sampler"], "gen_version": GEN_VERSION, "git_sha": R.GIT_SHA, "seed": SEED,
            "structure_hash": sha(json.dumps(b["M"], sort_keys=True, default=str) + json.dumps(b["P"]))[:16],
            "difficulty_bin": None, "crowd_pg": None, "depth": b["info"]["depth"], "deep": deep,
            "format_style": style["id"], "wording_id": w["id"], "defs_style": defs_style, "twin_of": twin_of,
            "twin_kind": twin_kind, "text_source": None, "licence": LICENCE,
            "edge": ["negation"] + sorted(set(fams)), "persona_seed": card["pack"]["persona_seed"]}
    return {"id": ids[t], "group_id": f"c_f5:g:{sha(pair_root)[:16]}", "call_id": f"c_f5:{sha(b['base_id'])[:12]}:{unit}",
            "source": SOURCE, "state": fields["state"], "qtype": "noul", "instructions": fields["instructions"],
            "options": None, "gold": gold, "role": rtype, "card": fields["card"], "meta": meta}


def side_record(b, t, row, q, k, fams, flips, key, push):
    card = b["card"]
    H = gen.H_for(card)
    aff = H.affixed_used(b["M"]) if hasattr(H, "affixed_used") else []
    nq = negc(q, aff)
    nt = negc(row["state"], aff)
    tag = H.tag_of(b["ctx"], b["P"], b["M"])
    pol = None if flips is None else flips % 2
    if t in ("V", "Vp") and b["cores"][b["vcore"]].rel == "other":
        vc = b["cores"][b["vcore"]]
        tag = vc.ptag                    # a V row about another atom: polarity of that atom's own predicate
        if tag is None:
            pol = None
    yib = None if (pol is None or tag is None) else ((tag == "bad") == (pol == 0))
    jq, jt = nq.k_all, nt.k_all
    loc = "none" if not jq and not jt else ("both" if jq and jt else ("question" if jq else "text"))
    return {"id": row["id"], "base_id": b["base_id"], "card_id": card["card_id"], "row_type": t, "k_neg": k,
            "k_syn": nq.k_syn, "k_all": nq.k_all, "j_q": jq, "j_t": jt, "t_txt": H.t_txt(b["M"]),
            "families": list(fams), "template": key, "core": key.split("|")[-2], "frame": None if key.startswith(
                ("mq", "C2m")) else "framed", "polarity_P": pol, "tag_P": tag, "yes_is_bad": bool(yib),
            "no_polarity": yib is None, "location": loc, "world_cell": card["world"],
            "card_form": "short" if b["defs_style"] == "short" else "full", "sem_keys": b["card_keys"],
            "base_depth": b["info"]["depth"], "v_P": b["v"], "gold": row["gold"], "attack_push": push,
            "pair_id": (sha(b["paired_with"]["base_id"])[:12] if "paired_with" in b else
                        (sha(b["base_id"])[:12] if "paired_with_p" in b else None)),
            "pair_change": b.get("pair_change"), "two_lcore": b.get("two_lcore", False), "sampler": card["sampler"],
            "wording": row["meta"]["wording_id"], "style": row["meta"]["format_style"], "inverted": card["inverted"],
            "fewshot": card.get("fewshot", False), "lf": b["rows"][t][1],
            "decoy": "C16" in fams or bool(b["M"].get("decoy_text")), "frame_id": frame_id(q),
            "vcore": b["vcore"] if t in ("V", "Vp") else None, "pair_member": "paired_with" in b or
            "paired_with_p" in b, "p_clause": next((c.clause for c in b["cores"].values()
                                                     if c.k == 0 and not c.fam and c.lf == b["P"]), None)}


def frame_id(q):
    from .forms import FRAMES
    import re as _re
    for fid, pat in FRAMES.items():
        rx = "^" + _re.escape(pat).replace(_re.escape("{c}"), ".+") + "$"
        if _re.match(rx, q):
            return fid
    return "C2m" if q.startswith("Is it false that ") else "mq"


def trim(bases, rows, rels, side, target, log, contrast_target=0.225):
    """Drop whole mirrored slot groups (a base, its antithetic twin in the partner card and any contrast-pair partner)
    in seeded order until the set holds at most `target` rows; balance by construction is kept. Repair r2 (XF03): each
    drop is taken from the unpaired groups while the contrast-set share is below 22.5% and from the contrast-pair
    groups otherwise, so the pool sits at the middle of the 20-25% band."""
    import random as _r
    rng = _r.Random(20261004)
    bmap = {b["base_id"]: b for b in bases}
    nrows, crows = collections.Counter(), collections.Counter()
    for r in rows:
        nrows[r["_bid"]] += 1
        b = bmap[r["_bid"]]
        if ("paired_with" in b or "paired_with_p" in b) and not r["id"].endswith("-Vp"):
            crows[r["_bid"]] += 1
    groups = groups_of(bases)
    rng.shuffle(groups)
    paired = [g for g in groups if any(crows[x] for x in g)]
    unpaired = [g for g in groups if not any(crows[x] for x in g)]
    drop = set()
    total, ctot = len(rows), sum(crows.values())
    while total > target and (paired or unpaired):
        lst = unpaired if (ctot / max(total, 1) < contrast_target and unpaired) or not paired else paired
        g = lst.pop()
        n = sum(nrows[x] for x in g)
        if total - n < target - 12:
            continue
        drop |= set(g)
        total -= n
        ctot -= sum(crows[x] for x in g)
    log["trimmed_bases"] = len(drop)
    log["contrast_share_after_trim"] = round(ctot / max(total, 1), 4)
    for b in bases:
        if b["base_id"] in drop:
            b.pop("ids", None)
    keep_rows = [r for r in rows if r["_bid"] not in drop]
    keep_ids = {r["id"] for r in keep_rows}
    return keep_rows, [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids], \
        [x for x in side if x["id"] in keep_ids]


G7_FEATURES, G7_ALPHA = 5000, 0.01     # F5 tests about 8,000-8,500 features at n >= 20; 5,000 keeps a margin


def card_passes_g7(n, y):
    """F5-R2-15: a feature present on every row of a card (a pack word) still passes G7's one-sided Bonferroni binomial
    (p0 = 1/2, alpha 0.01 Bonferroni over F5's feature count, taken as 5,000 < the ~8,500 tested) at the
    card's realized yes count."""
    from scipy.stats import binom
    m = max(y, n - y)
    return n == 0 or binom.sf(m - 1, n, 0.5) >= G7_ALPHA / G7_FEATURES


def groups_of(bases):
    """Whole mirrored slot groups: a base, its antithetic twin in the partner card and any contrast-pair partner."""
    by_slot = {(b["card"]["card_id"], b["slot"]["i"]): b for b in bases if "ids" in b}
    groups, seen = [], set()
    for b in sorted((b for b in bases if "ids" in b), key=lambda b: b["base_id"]):
        if b["base_id"] in seen:
            continue
        g, todo = set(), [b]
        while todo:
            x = todo.pop()
            if x is None or x["base_id"] in g or "ids" not in x:
                continue
            g.add(x["base_id"])
            todo += [x.get("paired_with"), x.get("paired_with_p"),
                     by_slot.get((x["card"]["partner"]["card_id"], x["slot"]["i"]))]
        seen |= g
        groups.append(sorted(g))
    return groups


def cap_trim(bases, rows, rels, side, log):
    """Repair r2 (F5-R2-15 G7 row cap, applied on the candidate pool so that every later selection obeys it): a card
    whose rows fail card_passes_g7 drops whole mirrored slot groups (unpaired groups first, seeded order), so the
    antithetic partner card drops the same slots and balance by construction is kept."""
    import random as _r
    rng = _r.Random(20261005)
    bid_card = {b["base_id"]: b["card"]["card_id"] for b in bases}
    n_rows, n_yes, rows_of = collections.Counter(), collections.Counter(), collections.Counter()
    for r in rows:
        c = bid_card[r["_bid"]]
        n_rows[c] += 1
        n_yes[c] += r["gold"]
        rows_of[r["_bid"]] += 1
    yes_of = collections.Counter()
    for r in rows:
        yes_of[r["_bid"]] += r["gold"]
    groups = groups_of(bases)
    rng.shuffle(groups)
    groups.sort(key=lambda g: len(g) > 2)          # unpaired groups (2 bases) before contrast-pair groups (4)
    drop = set()
    for c in sorted(n_rows):
        if card_passes_g7(n_rows[c], n_yes[c]):
            continue
        for g in groups:
            if card_passes_g7(n_rows[c], n_yes[c]):
                break
            if g[0] in drop or not any(bid_card[x] == c for x in g):
                continue
            drop |= set(g)
            for x in g:
                n_rows[bid_card[x]] -= rows_of[x]
                n_yes[bid_card[x]] -= yes_of[x]
        log["g7cap_cards"] += 1
    log["g7cap_bases_dropped"] = len(drop)
    log["g7cap_rows_dropped"] = sum(rows_of[x] for x in drop)
    for b in bases:
        if b["base_id"] in drop:
            b.pop("ids", None)
    keep_rows = [r for r in rows if r["_bid"] not in drop]
    keep_ids = {r["id"] for r in keep_rows}
    return keep_rows, [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids], \
        [x for x in side if x["id"] in keep_ids]


def zfilter(bases, rows, rels, side, log, max_drops=40):
    """Repair r2, G7 second line (spec G7: "matched twins first, z-filtering second"): after the matched-twin fixes
    (mirrored slots, shared card layout, pair orientation), any word unigram / bigram of the model-visible text (card +
    instructions + state; n >= 20) that still fails the one-sided binomial at alpha 0.01 / 5,000 is z-filtered by
    dropping whole mirrored slot groups (unpaired groups first) that carry the feature on its majority side, the
    group that removes the most excess per dropped row first; at most `max_drops` groups (logged)."""
    import re as _re
    from scipy.stats import binom
    tok = _re.compile(r"[a-z0-9]+")
    thr = G7_ALPHA / G7_FEATURES

    def feats(r):
        t = tok.findall("\n\n".join([r.get("card") or "", r["instructions"], r["state"]]).lower())
        return set(t) | {a + " " + b for a, b in zip(t, t[1:])}
    fr = {r["id"]: feats(r) for r in rows}
    n, y = collections.Counter(), collections.Counter()
    for r in rows:
        for f in fr[r["id"]]:
            n[f] += 1
            y[f] += int(r["gold"])
    bid_rows = collections.defaultdict(list)
    for r in rows:
        bid_rows[r["_bid"]].append(r)
    groups = groups_of(bases)
    paired_bids = {b["base_id"] for b in bases if "paired_with" in b or "paired_with_p" in b}

    def failing():
        out = []
        for f, k in n.items():
            if k >= 20:
                m = max(y[f], k - y[f])
                p = binom.sf(m - 1, k, 0.5)
                if p < thr:
                    out.append((p, f))
        return sorted(out)
    drop, dropped_for = set(), []
    for _ in range(max_drops):
        fl = failing()
        if not fl:
            break
        _, f = fl[0]
        sign = 1 if 2 * y[f] > n[f] else -1
        best = None
        for g in groups:
            if g[0] in drop:
                continue
            rr = [r for x in g for r in bid_rows[x]]
            ex = sum(sign * (2 * int(r["gold"]) - 1) for r in rr if f in fr[r["id"]])
            if ex <= 0:
                continue
            key = (any(x in paired_bids for x in g), -ex / len(rr))
            if best is None or key < best[0]:
                best = (key, g, rr)
        if best is None:
            break
        _, g, rr = best
        drop |= set(g)
        dropped_for.append(f)
        for r in rr:
            for h in fr[r["id"]]:
                n[h] -= 1
                y[h] -= int(r["gold"])
    log["zfilter_groups_dropped"] = len(dropped_for)
    log["zfilter_rows_dropped"] = sum(len(bid_rows[x]) for x in drop)
    log["zfilter_still_failing"] = len(failing())
    zfilter.last = sorted(set(dropped_for))
    for b in bases:
        if b["base_id"] in drop:
            b.pop("ids", None)
    keep_rows = [r for r in rows if r["_bid"] not in drop]
    keep_ids = {r["id"] for r in keep_rows}
    return keep_rows, [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids], \
        [x for x in side if x["id"] in keep_ids]


def cell_balance(bases, rows, rels, side, log, tol=0.02, max_rounds=400):
    """Repair r2 (G10 aggregate cell family x wording x bin x k_all, 50 +/- 2; bin is 'unscored' until G9): the spec's
    within-cell downsampling, applied to whole mirrored slot groups on the pool. Mirrored groups are balanced in every
    cell by construction except where the two cards' rows differ in k_all (pack words); a greedy pass drops the
    groups whose removal most reduces the summed excess over the tolerance per dropped row, until no cell is out."""
    sd = {x["id"]: x for x in side}
    bid_rows = collections.defaultdict(list)
    for r in rows:
        bid_rows[r["_bid"]].append(r)

    def cell(r):
        return (r["meta"]["wording_id"], sd[r["id"]]["k_all"])
    D, N = collections.Counter(), collections.Counter()
    for r in rows:
        D[cell(r)] += 2 * int(r["gold"]) - 1
        N[cell(r)] += 1
    groups = groups_of(bases)
    gv = []
    for g in groups:
        v, n = collections.Counter(), collections.Counter()
        for x in g:
            for r in bid_rows[x]:
                v[cell(r)] += 2 * int(r["gold"]) - 1
                n[cell(r)] += 1
        if any(v.values()):
            gv.append((g, v, n))

    def excess(c, d, nn):
        return max(0.0, abs(d) - 2 * tol * nn) if nn else 0.0
    drop = set()
    for _ in range(max_rounds):
        bad = {c for c in N if excess(c, D[c], N[c]) > 0}
        if not bad:
            break
        best = None
        for i, (g, v, n) in enumerate(gv):
            if g[0] in drop or not (set(v) & bad):
                continue
            gain = 0.0
            for c in set(v) | set(n):
                gain += excess(c, D[c], N[c]) - excess(c, D[c] - v[c], N[c] - n[c])
            size = sum(n.values())
            if gain > 1e-9 and (best is None or gain / size > best[0]):
                best = (gain / size, i)
        if best is None:
            break
        g, v, n = gv[best[1]]
        drop |= set(g)
        for c in set(v) | set(n):
            D[c] -= v[c]
            N[c] -= n[c]
    left = sum(1 for c in N if excess(c, D[c], N[c]) > 0)
    log["cellbal_bases_dropped"] = len(drop)
    log["cellbal_rows_dropped"] = sum(len(bid_rows[x]) for x in drop)
    log["cellbal_cells_still_out"] = left
    for b in bases:
        if b["base_id"] in drop:
            b.pop("ids", None)
    keep_rows = [r for r in rows if r["_bid"] not in drop]
    keep_ids = {r["id"] for r in keep_rows}
    return keep_rows, [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids], \
        [x for x in side if x["id"] in keep_ids]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True, choices=["candidates", "qc", "mixdev", "smoke"])
    ap.add_argument("--cards", type=int, default=None)
    ap.add_argument("--bases", type=float, default=None, help="bases per card")
    ap.add_argument("--samplers", default=None)
    ap.add_argument("--target", type=int, default=None, help="trim whole mirrored slot groups down to <= target rows")
    a = ap.parse_args(argv)
    t0 = time.time()
    log = collections.Counter()
    if a.set == "mixdev":
        from . import s5_hooks
        cards = s5_hooks.plan_dev_cards()
        n_per = lambda c: c["n_bases"]  # noqa: E731
        held = True
        tag = "dv"
    else:
        tag = {"candidates": "r1", "qc": "qc", "smoke": "sm"}[a.set]
        n_cards = a.cards or (122 if a.set != "smoke" else 8)
        cards = plan_cards(n_cards, seed_tag=tag)
        if a.samplers:
            keep = set(a.samplers.split(","))
            cards = [c for c in cards if c["sampler"] in keep]
        per = a.bases or {"candidates": 10.8, "qc": 10.2, "smoke": 4}[a.set]
        n_per = lambda c: int(round(per * (2.1 if c["sampler"] == "S2" else 1.0)))  # noqa: E731  (S2 length skips)
        held = False
    setup_cards(cards, tag)
    bases = phase1(cards, n_per, log)
    share = phase2(bases)
    rows, rels, side, fails = phase3(bases, held_out=held, set_tag=tag)
    if not held:
        rows, rels, side = cap_trim(bases, rows, rels, side, log)
    if a.target and len(rows) > a.target:
        rows, rels, side = trim(bases, rows, rels, side, a.target, log)
    if not held:
        rows, rels, side = zfilter(bases, rows, rels, side, log)
        rows, rels, side = cell_balance(bases, rows, rels, side, log)
    name = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5", "smoke": "smoke"}[a.set]
    OUT.mkdir(exist_ok=True)
    for r in rows:
        r.pop("_bid", None)
    write_jsonl(OUT / f"{name}.jsonl", rows)
    write_jsonl(OUT / f"{name}.relations.jsonl", rels)
    write_jsonl(OUT / f"{name}.F5_polarity.jsonl", side)
    write_jsonl(OUT / f"{name}.cards.jsonl", [card_summary(c) for c in cards])
    from .common import TMP
    write_jsonl(TMP / f"{name}.bases.jsonl", [{"base_id": b["base_id"], "sampler": b["card"]["sampler"],
                                               "inverted": b["card"].get("inverted", False), "M": b["M"],
                                               "P": b["P"], "ids": b.get("ids"), "v": b["v"]} for b in bases
                                              if "ids" in b])
    stats = {"rows": len(rows), "bases": len(bases), "relations": len(rels), "fails": dict(fails), "log": dict(log),
             "card_rule_sets": getattr(setup_cards, "last", None),
             "frame_share": share, "zfilter_features": getattr(zfilter, "last", []), "secs": round(time.time() - t0, 1)}
    json.dump(stats, open(OUT / f"{name}.buildstats.json", "w"), indent=1)
    print(json.dumps(stats, indent=1))
    progress(f"build {name}: {len(rows)} rows, {len(bases)} bases, fails {dict(fails)}, {stats['secs']}s")


if __name__ == "__main__":
    main()
