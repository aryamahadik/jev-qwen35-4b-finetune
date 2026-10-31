"""S7 codebook-card build (G0 section 3 S7). One worker per dataset group (XED; MAMS ACSA + ATSA; GHC) so the
one-claim-per-normalized-text rule holds across every F10 S7 group and example of that group (MAMS ACSA and ATSA share
sentences). EDOS: formats-2 marks no EDOS record F10_S7-eligible (no per-annotator file listed in register row 17,
X15 / R5-F), so no EDOS row or example is built; logged once and reported (F10 moves no share on its own).
Every row passes fmt1 loader_check (G15, check_rows on the A16 trainer), the S7 parse (G3: codebook text read back
through the lexicon + connective registry, byte-for-byte coded text, ATSA frame) and the first-fit re-solve on the
parsed codebook (G2); a failing row is dropped with its group and counted as a generator bug."""
from __future__ import annotations

import itertools
import traceback
from collections import Counter

import lexicon as L
import parse_s7 as PS
import pools
import s7 as S
from common import FAMILY, GEN_VERSION, GIT_SHA, SPEC_ID, rng, uhash
from samplers import bucket_of, note_yn

GROUPS = {"xed": ["xed"], "mams": ["mams_acsa", "mams_atsa"], "ghc": ["ghc"]}
LARGE_ROWS = {"xed": 100, "mams": 100}          # rows on each >= 20-code codebook card (r1 candidates)
DATASET_ROWS = 405                               # r1 candidates per dataset (1.5 x 270)
CHOICE_LARGE, CHOICE_SMALL = 0.72, 0.42          # per-card choice share: the 10-19 / 20-60 buckets need large cards


def s7_plan(tag):
    """Cards: one per ready F10 codebook; rows per dataset 405 (r1) or scaled (qc); modes 40/30/30 neutral/swapped/
    natural over cards; examples on 50% of cards (only codebooks of <= 9 codes can print them)."""
    r = rng("s7plan", "r1")
    cbs = sorted(S.codebooks(), key=lambda c: c["id"])
    scale = 1.0 if tag == "r1" else 5200 / 4995
    cards = []
    for g, schemes in GROUPS.items():
        mine = [c for c in cbs if c["scheme"] in schemes]
        large = [c for c in mine if len(c["codes"]) >= 20]
        small = [c for c in mine if len(c["codes"]) < 20]
        left = DATASET_ROWS - LARGE_ROWS.get(g, 0) * len(large)
        for c in large:
            cards.append({"cb": c["id"], "group": g, "n_rows": round(LARGE_ROWS[g] * scale), "choice_share": CHOICE_LARGE})
        for i, c in enumerate(small):
            n = left // len(small) + (1 if i < left % len(small) else 0)
            cards.append({"cb": c["id"], "group": g, "n_rows": round(n * scale), "choice_share": CHOICE_SMALL})
    n = len(cards)
    # name modes 40 / 30 / 30 of S7 CHOICE rows: greedy on expected choice rows (largest card to largest deficit)
    w = {i: c["n_rows"] * c["choice_share"] for i, c in enumerate(cards)}
    tot = sum(w.values())
    left = {"neutral": 0.4 * tot, "swapped": 0.3 * tot, "natural": 0.3 * tot}
    modes = [None] * n
    order = sorted(range(n), key=lambda i: (-w[i], r.random()))
    for i in order:
        m = max(left, key=lambda k: (left[k], r.random()))
        modes[i] = m
        left[m] -= w[i]
    exable = [i for i, c in enumerate(cards) if len(next(x for x in cbs if x["id"] == c["cb"])["codes"]) <= 9]
    ex_on = set(r.sample(exable, round(0.5 * n)))
    for i, c in enumerate(cards):
        c["idx"] = i
        c["mode"] = modes[i]
        c["ex_on"] = i in ex_on
    return cards


def ghc_perm(card, r):
    """C12 (GHC): a permutation of the non-residual code names whose code-level name prior (name at gold's position
    is gold's own natural name) and side-level prior (that name's side equals gold's side) are each near 50% under
    uniform gold; chosen among all permutations, ties broken by the seeded draw."""
    codes = card["codes"]
    nonres = [i for i, c in enumerate(codes) if not c["residual"]]
    side = {i: S.code_polarity(codes[i], r) or "not bad" for i in nonres}
    best, key = None, None
    perms = list(itertools.permutations(nonres))
    r.shuffle(perms)
    for p in perms[:5000]:
        fix = sum(a == b for a, b in zip(nonres, p)) / len(nonres)
        sm = sum(side[a] == side[b] for a, b in zip(nonres, p)) / len(nonres)
        k = abs(fix - 0.5) + abs(sm - 0.5)
        if key is None or k < key:
            best, key = p, k
    names = [c["natural_name"] for c in codes]
    out = list(names)
    for pos, src in zip(nonres, best):
        out[pos] = names[src]
    return out


def card_worker(args):
    pcs, tag, prefix = args
    try:
        return _group_worker(pcs, tag, prefix)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:], "plan": pcs[0]}


def _group_worker(pcs, tag, prefix):
    cbs = {c["id"]: c for c in S.codebooks()}
    claimed = set()
    pools7 = {}
    out = []
    for pc in pcs:
        cb = cbs[pc["cb"]]
        scheme = cb["scheme"]
        if scheme not in pools7:
            pools7[scheme] = S.Pool7(scheme, claimed)
        pool = pools7[scheme]
        out.append(one_card(pc, cb, pool, tag, prefix))
    return {"cards": out, "drops": {s: dict(p.drops) for s, p in pools7.items()}, "claims": len(claimed)}


def one_card(pc, cb, pool, tag, prefix):
    r = rng("s7card", tag, cb["id"], pc["idx"])
    stats = Counter()
    card = S.build_s7_card(cb, pc["idx"], pc["mode"], r, pc["ex_on"])
    if tag != "r1":
        card["card_id"] += f"-{tag}"
    if pc["mode"] == "swapped" and cb["scheme"] == "ghc":
        card["names"] = ghc_perm(card, r)
        card["qnames"] = [card["qform"].format(n=x) for x in card["names"]]
    idx = pool.index(card["codes"])
    S.add_examples(card, pool, idx, r)
    # card-fixed styles (>= 5) and wordings (>= 5: 4-5 any-form + 1 yes/no-form)
    sty = [s for m, ss in pools.styles().items() for s in ss]
    sty.sort(key=lambda s: s["id"])
    card["styles"] = r.sample(sty, 6)
    wds = pools.wordings()[0]
    anyw = [w for w in wds if w["forms"] == ["any"]]
    card["wordings"] = r.sample(anyw, r.choice([4, 5])) + r.sample([w for w in wds if w["forms"] == ["yn"]], 1)
    plan = {"n_rows": pc["n_rows"], "choice_share": pc["choice_share"], "yes_rate": r.uniform(0.2, 0.8),
            "twin_p": 0.22, "neg_p": 0.16, "dneg_p": 0.05}
    rows, sides, rels = [], [], []
    plan["_fb"] = True     # repair r1 (G10 abstain): the residual-gold controller counts emitted choice rows only
    for group in S.s7_groups(card, pool, idx, r, plan, stats):
        res = render_group(card, cb, group, r, stats, prefix)
        if res is None:
            continue
        ids = {x["id"] for x in res[0]}
        for sp in group:
            if sp.get("form") == "choice" and sp.get("_rid") in ids:
                S.s7_note_choice(plan, sp)
        rows += res[0]
        sides += res[1]
        rels += res[2]
        note_yn(plan, res[0])     # repair r1 (G7): feedback for the per-card yes-rate controller
    summ = {"card_id": card["card_id"], "sampler": "S7", "ctype": "codebook", "scheme": cb["scheme"],
            "codebook": cb["id"], "mode": card["mode"], "n_codes": len(card["codes"]),
            "examples": len(card.get("examples", [])), "styles": [s["id"] for s in card["styles"]],
            "wordings": [w["id"] for w in card["wordings"]], "rows": len(rows),
            "example_claims": [e["norm"] for e in card.get("examples", [])]}
    return {"rows": rows, "sides": sides, "rels": rels, "card": summ, "stats": dict(stats)}


def render_group(card, cb, group, r, stats, prefix):
    from fmt1 import card as fcard
    import negcount
    gid = f"{prefix}{card['card_id']}-{group[0]['gid']:03d}"
    anchor_id = gid + "-a"
    rows, sides, rels = [], [], []
    for j, spec in enumerate(group):
        rid = anchor_id if j == 0 else f"{gid}-{spec.get('twin_kind', 'x')[:2]}{j}"
        spec["_rid"] = rid
        short = uhash(rid, "short") < 0.15
        st = card["styles"][int(uhash(rid, "st") * len(card["styles"]))]
        want = ("any", "yn") if spec["form"] == "yn" else ("any",)
        wl = [w for w in card["wordings"] if w["forms"][0] in want]
        # G11 (repair r1): cycle through the card's wordings for the form (hashed start)
        ctr = card.setdefault("_wdctr", {})
        wi = ctr.get(want, int(uhash(card["card_id"], "wd0", "|".join(want)) * len(wl)))
        ctr[want] = wi + 1
        wd = wl[wi % len(wl)]
        row, ir, q, layout = S.render_row(card, spec, rid, st, wd["text"], short)
        res = fcard.loader_check(row, must_show=fcard.must_show(ir, question=q, wording=wd["text"]))
        if not res["ok"]:
            stats["loader_fail"] += 1
            stats["loader_fail:" + "|".join(res["problems"])[:80]] += 1
            if j == 0:
                return None
            continue
        probs, h = PS.g3_s7(row, card, spec, spec["rec"])
        if probs:
            stats["g3_fail"] += 1
            stats["g3_fail:" + probs[0][:90]] += 1
            if j == 0:
                return None
            continue
        nc = negcount.count(q)
        rec = spec["rec"]
        tk = spec.get("twin_kind") if j else None
        meta = {"family": FAMILY, "spec_id": SPEC_ID, "card_id": card["card_id"],
                "domain_pack": f"{cb['dataset']}:{cb['id']}", "sampler": "S7", "gen_version": GEN_VERSION,
                "git_sha": GIT_SHA, "seed": int(uhash(rid, "seed") * 2 ** 31), "structure_hash": h,
                "difficulty_bin": None, "crowd_pg": None, "depth": 1, "deep": False, "format_style": st["id"],
                "wording_id": wd["id"], "defs_style": "codebook_examples" if card.get("examples") else "codebook",
                "twin_of": None if j == 0 else anchor_id, "twin_kind": tk,
                "text_source": {"dataset": cb["dataset"], "record_id": rec["record_id"], "split": "train"},
                "licence": S.LICENCE[card["scheme"]], "edge": [f"layout:{layout}"]}
        call = gid + "-u" if (j == 0 or spec.get("rel")) else f"{gid}-t{j}"
        rows.append({"id": rid, "group_id": gid, "call_id": call, "source": "c_own_F10", "state": row["state"],
                     "qtype": row["qtype"], "instructions": row["instructions"], "options": row["options"],
                     "gold": row["gold"], "role": "base" if j == 0 else tk, "card": row["card"], "meta": meta})
        sides.append(side_entry(card, spec, rid, gid, anchor_id, nc, row, st, wd, layout, short))
        if j and spec.get("rel"):
            rels.append({"a": anchor_id, "b": rid, "type": spec["rel"]})
    if not rows or rows[0]["id"] != anchor_id:
        return None
    return rows, sides, rels


def name_prior7(card, spec):
    """Code the name alone points to: the shown option whose name is the natural name of the record's natural-mode
    first-fit code (swapped cards only)."""
    if card["mode"] != "swapped" or spec["form"] != "choice":
        return None
    codes = card["codes"]
    g_nat = S.first_fit(codes, spec["rec"], spec["ti"], card["scheme"])
    nat = codes[g_nat]["natural_name"]
    for i in spec["options"]:
        if card["names"][i] == nat:
            return int(i == spec["gold"])
    return None


def side_entry(card, spec, rid, gid, anchor_id, nc, row, st, wd, layout, short):
    k = len(row["options"]) if row["qtype"] == "choice" else 2
    e = {"id": rid, "sel_unit": gid, "sel_anchor": anchor_id, "sampler": "S7", "card_id": card["card_id"],
         "form": spec["form"], "mode": card["mode"], "world": None, "ctype": "codebook", "scheme": card["scheme"],
         "wkind": "fits" if spec["form"] == "yn" else None, "neg": spec.get("neg", 0), "k_syn": nc.k_syn,
         "k_all": nc.k_all, "k": k, "bucket": bucket_of(k) if row["qtype"] == "choice" else None, "layout": layout,
         "style": st["id"], "wording_id": wd["id"], "short": short, "twin_kind": spec.get("twin_kind"),
         "rel": spec.get("rel"), "attack": None, "inert": False, "name_prior": name_prior7(card, spec),
         "record_norm": spec["rec"]["norm_sha256"], "record_class": record_class(card["scheme"], spec)}
    if spec["form"] == "yn":
        tag = card["polarity"][spec["ask"]]
        e["polarity_tag"] = tag
        e["yes_bad"] = (tag == "bad") if spec.get("neg", 0) in (0, 2) else (tag != "bad")
        e["asked_pos"] = spec["ask"]
    else:
        g = spec["gold"]
        res = card["codes"][g]["residual"]
        e["gold_kind"] = "abstain" if res else "term"
        e["abstain_shown"] = ["residual"]
        e["gold_pos"] = None if res else g
        e["n_terms_card"] = len(card["codes"]) - 1
    return e


def record_class(scheme, spec):
    a = spec["rec"]["ann"]
    if scheme == "xed":
        return sorted(a.get("emotions") or ["neutral"]) if isinstance(a, dict) else None
    if scheme == "mams_atsa":
        return a["terms"][spec["ti"]].get("polarity")
    if scheme == "mams_acsa":
        return sorted(f"{c}:{p}" for c, p in a.get("aspects", []))
    return "+".join(sorted(k for k, v in a.items() if v)) or "none"
