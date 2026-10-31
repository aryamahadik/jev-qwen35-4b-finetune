"""Program-card build (S1-S4, S6): one worker call per card -> rows, side manifest, relations, card summary.
Every row passes fmt1 loader_check (pinned check_rows), G3 parse + structure hash, and G2 (solver B on the parse)
before it is kept; a failing row is logged as a generator bug and dropped with its whole group."""
from __future__ import annotations

import copy
import json
import traceback
from collections import Counter

import cardgen as C
import cardtext as T
import emit as EM
import g3 as G3
import model as M
import packs_f10 as P
import pools
from common import FAMILY, GEN_VERSION, GIT_SHA, LIC_PROGRAM, SPEC_ID, rng, uhash
from plan import k_drawer
from samplers import ProgRows, bucket_of, note_yn


def card_meta_base(card, pack):
    return {"family": FAMILY, "spec_id": SPEC_ID, "card_id": card["card_id"], "domain_pack": pack["pack_id"],
            "sampler": card["sampler"], "gen_version": GEN_VERSION, "git_sha": GIT_SHA}


def fewshot_for(card, r):
    from examples import _point_in
    cs = __import__("cases").Cases(card, r)
    out = []
    from examples import one_line
    tries = 0
    while len(out) < r.choice([1, 2, 3]) and tries < 30:
        tries += 1
        t = r.choice(card["order"])
        case = cs.point(cs.region_for(t))
        if case is None:
            continue
        rec = one_line(card, sorted(card["legend"]), case)
        if r.random() < 0.5 and card["ctype"] in ("amo", "first", "partition", "dlist"):
            q = "Which term does this card assign to it?" if card["sampler"] != "S3" else "Which code does it get?"
            ans = card["names"][cs.answer(case).pop()]
            kind = "choice"
        else:
            X = r.choice(card["order"])
            q = f"Does it meet the definition of {card['names'][X]}?" if card["sampler"] != "S3" else \
                f"Does it meet the conditions of row {card['names'][X]}?"
            ans = "Yes" if cs.mc.meets(X, case) else "No"
            kind = "meets"
        out.append({"case_text": rec[0].upper() + rec[1:] + ".\n" + q, "answer": ans, "kind": kind,
                    "case": {str(k): v for k, v in case.items()}})
    return out


def card_worker(args):
    """args: (plan card dict, pack id, seed tag, id prefix). Returns dict with rows, sides, rels, card summary, stats."""
    pc, pack_id, tag, prefix = args
    try:
        # a card whose 240 structure draws all fail is redrawn whole with a fresh seed salt (logged in the summary),
        # never dropped; the plan (sampler, ctype, k, world, mode, flags) stays the same
        # If every salt fails at the plan's k (e.g. a swapped-mode card whose trimmed legend leaves too few label
        # words for k terms plus helpers), k drops by one, then two, but never out of the plan's k bucket (logged)
        k0 = pc.get("k")
        ks = [k0] + ([kk for kk in (k0 - 1, k0 - 2) if _bucket(kk) == _bucket(k0)] if isinstance(k0, int) else [])
        for kk in ks:
            for salt in [pc.get("salt")] + [f"cd{i}" for i in range(1, 7)]:
                p2 = dict(pc, k=kk)
                res = _card_worker(dict(p2, salt=salt) if salt else p2, pack_id, tag, prefix)
                if res.get("error") != "card draw failed":
                    if "card" in res:
                        res["card"]["card_salt"] = salt
                        res["card"]["k_reduced_from"] = k0 if kk != k0 else None
                    return res
        return res
    except Exception as e:  # a generator bug: report it, never hide it
        return {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:], "plan": pc}


def probe_kmax(args):
    """The card draw of card_worker only (same salts, same k fallbacks, same seeds), no rows: returns the drawn card's
    term count + its open-world abstain slot, so plan.set_kshares can spread each sampler's option-bucket shares
    over what the cards can really show (repair r1, G10 option buckets)."""
    pc, pack_id, tag, prefix = args
    tr, ho = P.load()
    pack = tr.get(pack_id) or ho[pack_id]
    k0 = pc.get("k")
    ks = [k0] + ([kk for kk in (k0 - 1, k0 - 2) if _bucket(kk) == _bucket(k0)] if isinstance(k0, int) else [])
    for kk in ks:
        for salt in [pc.get("salt")] + [f"cd{i}" for i in range(1, 7)]:
            p2 = dict(pc, k=kk)
            if salt:
                p2["salt"] = salt
            r = rng("card", tag, p2["sampler"], p2["idx"], pack_id, *([p2["salt"]] if p2.get("salt") else []))
            card = C.build_program_card(p2, pack, r)
            if card is not None:
                return pc["ordinal"], len(card["order"]) + (1 if card["world"] == "open" else 0)
    return pc["ordinal"], None


def _bucket(k):
    return 0 if k <= 4 else 1 if k <= 9 else 2 if k <= 19 else 3


def _card_worker(pc, pack_id, tag, prefix):
    tr, ho = P.load()
    pack = tr.get(pack_id) or ho[pack_id]
    r = rng("card", tag, pc["sampler"], pc["idx"], pack_id, *([pc["salt"]] if pc.get("salt") else []))
    stats = Counter()
    card = C.build_program_card(pc, pack, r)
    if card is None:
        return {"error": "card draw failed", "plan": pc}
    card["card_id"] = f"F10-{pc.get('label', pc['sampler'])}-{pc['idx']:02d}" + ("" if tag in ("r1", "s5") else f"-{tag}")
    if pc.get("faq"):
        card["faq"] = True     # S5 held-out FAQ glossary (dev only)
    card["ordinal"] = pc.get("ordinal", pc["idx"])
    for k in ("examples_on", "conseq_on", "prose_record", "inverted"):
        card[k] = pc.get(k, False)
    if card["sampler"] == "S6":
        card["prose_record"] = False
    wds = pools.wordings()[0]
    styles = pools.styles(held_out=pc.get("held_out", False))
    T.prepare_card(card, r, pack, styles, wds)
    T.add_examples(card, r)
    if pc.get("fewshot"):
        card["fewshot"] = fewshot_for(card, r)
    plan = dict(pc)
    plan["yes_rate"] = r.uniform(0.2, 0.8)
    plan["choice_share"] = 0.56   # neg/dneg twins are yes/no rows: 0.56 keeps the family near 50% choice
    # repair r1: choice-type rows per card (forward choice + inverted, twins included) are controlled at these shares
    plan["choice_rows"] = 0.60 if card.get("inverted") else 0.50
    plan["draw_k"] = k_drawer(card["sampler"], r, len(card["order"]), 1 if card["world"] == "open" else 0,
                              pc.get("kshare"))
    plan["inv_kmax"] = 9
    plan.setdefault("twin_p", 0.20)
    plan.setdefault("neg_p", 0.14)
    plan.setdefault("dneg_p", 0.05)
    plan.setdefault("nameinv_p", 0.07)
    plan.setdefault("attack_p", 0.09)
    plan.setdefault("attack_p_yn", 0.30)   # repair r1: attack units on yes/no rows only (G7)
    if card["sampler"] == "S6":
        import s6
        gen = s6.s6_rows(card, r, plan, stats)
    else:
        pr = ProgRows(card, r, stats)
        plan["_fb"] = True     # repair r1 (G10 abstain): the abstain-gold controller counts emitted choice rows only
        gen = pr.groups(plan)
    rows, sides, rels = [], [], []
    plan["_emitted"] = 0
    seen = set()
    for group in gen:
        sh0 = card.get("_short", [0])[0]
        out = render_group(card, pack, group, r, stats, prefix, plan)
        if out is None:
            if "_short" in card:
                card["_short"][0] = sh0
            continue
        g_rows, g_sides, g_rels = out
        # G12 (repair r1): one surface form per structure. A group whose structure_hash repeats one of an earlier
        # group of this card is not emitted and the sampler draws another group (twins inside a group may share it)
        hs = {x["meta"]["structure_hash"] for x in g_rows}
        if hs & seen:
            stats["dup_structure_redrawn"] += 1
            card["_short"][0] = sh0
            continue
        seen |= hs
        card["_short"][0] = sh0 + len(g_rows)
        rows += g_rows
        sides += g_sides
        rels += g_rels
        plan["_emitted"] += len(g_rows)
        note_yn(plan, g_rows)     # repair r1 (G7): feedback for the per-card yes-rate controller
        if plan.get("_fb"):
            ids = {x["id"] for x in g_rows}
            for sp in group:
                if sp.get("form") == "choice" and sp.get("_rid") in ids:
                    pr.note_choice(sp)
    summ = {"card_id": card["card_id"], "sampler": card["sampler"], "ctype": card["ctype"], "world": card["world"],
            "mode": card["mode"], "pack": pack_id, "n_terms": len(card["order"]), "classes": card["classes"],
            "rules": [i for i, _ in card["rules"]], "examples": bool(card.get("examples_on")),
            "fewshot": bool(card.get("fewshot")), "inverted": bool(card.get("inverted")),
            "conseq": bool(card.get("conseq")), "lookalike": bool(card.get("lookalike")),
            "defs_style": defs_style(card), "dv": card["rc"].get("dv"), "styles": card["rc"]["styles"],
            "wordings": [w["id"] for w in card["rc"]["wordings"]], "persona_seed": pack["persona_seed"],
            "redraws": card.get("redraws"), "rows": len(rows), "prose_record": bool(card.get("prose_record")),
            "faq": bool(card.get("faq")), "pack_attrs": {a["name"]: a["lex"] for a in card["legend"].values()}}
    return {"rows": rows, "sides": sides, "rels": rels, "card": summ, "stats": dict(stats)}


def defs_style(card):
    ex = bool(card.get("examples_on")) and any(card.get("examples", {}).values())
    if card["sampler"] == "S3":
        return "table_examples" if ex else "table"
    return "one_line_examples" if ex else "one_line"


def nameinv_word(card, pack, X, r):
    used = set(card["names"].values())
    cands = [w["word"] for w in pack["label_words"] if w["word"] not in used]
    r.shuffle(cands)
    for w in cands:
        if C.name_lint(w, card["legend"], pack, [n for t, n in card["names"].items() if t != X]):
            return w
    return None


def render_group(card, pack, group, r, stats, prefix, plan):
    gid = f"{prefix}{card['card_id']}-{group[0]['gid']:03d}"
    anchor_id = gid + "-a"
    rows, sides, rels = [], [], []
    import negcount
    for j, spec in enumerate(group):
        rid = anchor_id if j == 0 else f"{gid}-{spec.get('twin_kind', 'x')[:2]}{j}"
        spec["_rid"] = rid
        # short-card rows: 15% of each card's emitted rows (G10 15 +/- 2 per sampler; repair r1: a per-card
        # low-discrepancy sequence with a hashed phase instead of an independent 15% coin per row)
        sh = card.setdefault("_short", [0, uhash(card["card_id"], "shortphase")])
        spec["short"] = int(0.15 * (sh[0] + 1) + sh[1]) > int(0.15 * sh[0] + sh[1])
        spec["u1_try"] = uhash(rid, "u1") < 0.30
        spec["inert"] = card["sampler"] == "S4" and uhash(rid, "inert") < 0.30
        if spec.get("nameinv"):
            w = nameinv_word(card, pack, spec["ask"], r)
            if w is None:
                stats["nameinv_noword"] += 1
                continue
            spec["nameinv_word"] = w
        try:
            row, side, c_shown = EM.render_spec(card, spec, rid, pack, r, plan)
        except Exception as e:
            stats["render_fail"] += 1
            stats["render_fail:" + type(e).__name__ + ":" + str(e)[:60]] += 1
            if j == 0:
                return None
            continue
        if not side["loader_ok"]:
            stats["loader_fail"] += 1
            stats["loader_fail:" + "|".join(side["loader_problems"])[:80]] += 1
            if j == 0:
                return None
            continue
        st = EM.pool.style(side["style"])
        pack_attrs = {a["name"]: a["lex"] for a in c_shown["legend"].values()}
        probs, h = G3.g3_row(row, spec, c_shown, st["container"], pack_attrs)
        if probs:
            stats["g3_fail"] += 1
            stats["g3_fail:" + probs[0][:90]] += 1
            if j == 0:
                return None
            continue
        q = side["question"]
        nc = negcount.count(q)
        depth = row_depth(c_shown, spec)
        meta = card_meta_base(card, pack)
        meta.update({"seed": int(uhash(rid, "seed") * 2 ** 31), "structure_hash": h, "difficulty_bin": None,
                     "crowd_pg": None, "depth": depth, "deep": depth >= 4, "format_style": side["style"],
                     "wording_id": side["wording_id"], "defs_style": defs_style(card),
                     "twin_of": None if j == 0 else anchor_id, "twin_kind": spec.get("twin_kind") if j else None,
                     "text_source": None, "licence": LIC_PROGRAM, "edge": [f"layout:{side['layout']}"],
                     "persona_seed": pack["persona_seed"]})
        if card["sampler"] == "S6":
            meta["subtype"] = "label_description"
        tk = spec.get("twin_kind") if j else None
        call = gid + "-u" if (j == 0 or spec.get("rel")) else f"{gid}-t{j}"
        out = {"id": rid, "group_id": gid, "call_id": call, "source": "c_own_F10", "state": row["state"],
               "qtype": row["qtype"], "instructions": row["instructions"], "options": row["options"],
               "gold": row["gold"], "role": "base" if j == 0 else tk, "card": row["card"], "meta": meta}
        rows.append(out)
        sides.append(side_entry(card, c_shown, spec, side, rid, gid, anchor_id, nc, row))
        card["_short"][0] += 1
        if j and spec.get("rel"):
            rels.append({"a": anchor_id, "b": rid, "type": spec["rel"]})
    rows, sides, rels = cap_long_units(rows, sides, rels, stats)
    if rows and rows[0]["id"] != anchor_id:
        return None
    return rows, sides, rels


def cap_long_units(rows, sides, rels, stats):
    """G15 (v2): every relation unit has <= 3 rows, and a unit with a row of >= 2,000 served tokens (real tokenizer,
    `instructions` counted twice, qc/gates.served_tokens) has <= 2 rows. A long 3-row unit keeps its anchor and the
    double-negated twin (the affirmative-twin pair of the negation quota); the single-negation twin, else the last
    twin, is not emitted (counted in stats)."""
    units = Counter(x["call_id"] for x in rows)
    if max(units.values(), default=0) <= 2:
        return rows, sides, rels
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "qc"))
    from gates import served_tokens
    drop = set()
    for cid, n in units.items():
        if n <= 2:
            continue
        idx = [i for i, x in enumerate(rows) if x["call_id"] == cid]
        if max(served_tokens(rows[i]) for i in idx) < 2000:
            continue
        twins = [i for i in idx if i != 0]
        pick = [i for i in twins if rows[i]["meta"].get("twin_kind") == "neg"] or twins[::-1]
        for i in pick[:n - 2]:
            drop.add(i)
            stats["long_unit_twin_dropped"] += 1
    if not drop:
        return rows, sides, rels
    gone = {rows[i]["id"] for i in drop}
    keep = [i for i in range(len(rows)) if i not in drop]
    return [rows[i] for i in keep], [sides[i] for i in keep], [x for x in rels if x["b"] not in gone]


def row_depth(c, spec):
    if spec["form"] == "inv" or c["sampler"] == "S6":
        defs = c["defs"]
        if spec["form"] == "inv":
            return 1 + max(M.nest(defs, spec["ask"]), 0)
        req = spec["options"] if spec["form"] == "choice" else [spec["ask"]]
        return 1 + max(M.nest(defs, t) for t in req if t in defs)
    mc = M.Card(c["defs"], c["order"])
    if spec["form"] == "choice":
        req = [o for o in spec["options"] if o in c["defs"]]
        if c["ctype"] in ("first", "dlist") and spec["gold"] in c["order"]:
            req += c["order"][:c["order"].index(spec["gold"])]
        if spec["gold"] == "none":
            req = list(c["order"])
    else:
        req = [spec["ask"]]
        if spec["wkind"] == "assigned" and c["ctype"] in ("first", "dlist"):
            req += c["order"][:c["order"].index(spec["ask"])]
    case = {k: v for k, v in spec["case"].items() if k not in spec.get("omitted", [])}
    return M.depth(mc, c["legend"], case, spec.get("omitted", []), sorted(set(req)))


def name_prior(c, spec):
    nat = c.get("natural")
    if not nat or c["mode"] != "swapped" or spec["form"] == "inv" or c["sampler"] == "S6":
        return None
    order = c["order"]
    if spec.get("omitted"):
        return "undetermined"
    met = []
    for t in order:
        d = nat.get(c["names"][t])
        if d is not None and M.Card({"np": d}, ["np"]).meets("np", spec["case"]):
            met.append(t)
    if spec["form"] == "choice":
        if c["ctype"] in ("first", "dlist"):
            return met[0] if met else "none"
        return "undetermined" if len(met) > 1 else (met[0] if met else "none")
    X = spec["ask"]
    if spec["wkind"] == "assigned" and c["ctype"] in ("first", "dlist"):
        v = bool(met) and met[0] == X
    else:
        v = X in met
    v = v if spec.get("neg", 0) in (0, 2) else not v
    return int(v)


def side_entry(card, c, spec, side, rid, gid, anchor_id, nc, row):
    form = spec["form"]
    k = len(row["options"]) if row["qtype"] == "choice" else 2
    e = {"id": rid, "sel_unit": gid, "sel_anchor": anchor_id, "sampler": card["sampler"], "card_id": card["card_id"],
         "form": form, "mode": card["mode"], "world": card["world"], "ctype": card["ctype"],
         "wkind": spec.get("wkind"), "neg": spec.get("neg", 0), "k_syn": nc.k_syn, "k_all": nc.k_all,
         "k": k, "bucket": bucket_of(k) if row["qtype"] == "choice" else None, "layout": side["layout"],
         "style": side["style"], "wording_id": side["wording_id"], "short": bool(spec.get("short")),
         "omitted": spec.get("omitted", []), "threshold": spec.get("threshold") is not None,
         "u1": spec.get("u1") is not None, "attack": side.get("attack"), "inert": side.get("inert"),
         "twin_kind": spec.get("twin_kind"), "rel": spec.get("rel"), "ecodes": spec.get("ecodes"),
         "name_prior": name_prior(c, spec), "override_words": card.get("helper_words") or [],
         "lookalike": bool(card.get("lookalike")), "conseq_visible": bool(card.get("conseq")),
         "fewshot_card": bool(card.get("fewshot")), "inverted_card": bool(card.get("inverted")),
         "rewrites": spec.get("rewrites")}
    if form == "yn":
        tag = card["polarity"][spec["ask"]]
        e["polarity_tag"] = tag
        e["yes_bad"] = (tag == "bad") if spec.get("neg", 0) in (0, 2) else (tag != "bad")
        e["asked_pos"] = card["order"].index(spec["ask"])
    elif form == "choice":
        g = spec["gold"]
        e["gold_kind"] = "abstain" if g in ("none", "cbd") else "term"
        e["abstain_shown"] = [o for o in spec["options"] if o in ("none", "cbd")]
        e["gold_pos"] = card["order"].index(g) if g in card["order"] else None
        e["n_terms_card"] = len(card["order"])
    else:
        e["gold_pos"] = spec["gold_idx"]
    return e
