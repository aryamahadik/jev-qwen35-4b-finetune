"""Cue template bank (G0 section 4) and the hard-negation probe hold-out.

A cue template = one question-side operator realization: (family, core template, position m = matrix interrogative /
e = embedded declarative, atom kind). Each declares its LF signature (the core's LF over <P>), k, slot monotonicity
(up / down / non-monotone-or-opaque), L_neg entries and N / D eligibility. The bank is enumerated from the generator's
own core builders over a dry run of bases on every sampler (no rows written), plus the C2 operators (C2n / C2f
embedded, C2m matrix). Question templates = the compositions actually emitted (outer class x C2 prefix stack x cue
template); G11's 2% rule applies to frame x question template.

Probe hold-out: 25 cue templates by a stratified seeded draw (at most floor(1/3) of any family's templates, at least
1 from each of >= 10 families), frozen with sha256 before any training row; training never uses them.

  python -m gen.bank            # enumerate, draw, write out/cue_bank.json
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import re

from .common import OUT, SEED, rng_for

BANK_FILE = OUT / "cue_bank.json"
_HELD = None


def norm_tid(tid):
    t = tid.split(":")[0]
    t = re.sub(r"\.\d+$", "", t)
    return t


def atom_kind(lf):
    while lf[0] == "not":
        lf = lf[1]
    if lf[0] == "and":
        return "conn:" + atom_kind(lf[1])
    if lf[0] == "ev":
        return "ev:" + lf[1].split(":")[0]
    if lf[0] == "grp":
        return "grp:" + lf[3][0]
    return lf[0]


ID_FAMILY = [("AMT", "C9"), ("EV.pos", "C10"), ("EV.pas", "C10"), ("Q.every", "C8"), ("Q.all", "C8"), ("Q.some", "C8"), ("Q.atleast", "C9"),
             ("Q.atmost", "C9"), ("Q.morehalf", "C9"), ("DEON.", "C12"), ("VAL.pos", "ID"), ("ADJ.pos", "ID"),
             ("HAS.pos", "ID"), ("INV.pos", "C11"), ("ST.pos", "C7")]


def family_of(core):
    if core.fam:
        return "+".join(core.fam)
    for pre, f in ID_FAMILY:
        if core.tid.startswith(pre):
            return f
    return "ID"


def keys_of(core):
    """Template keys of a core: one per position it can take."""
    fam = family_of(core)
    base = f"{fam}|{norm_tid(core.tid)}|{atom_kind(core.lf)}"
    out = [base + "|e"]
    if core.matrix:
        out.append(base + "|m")
    return out


def held():
    global _HELD
    if _HELD is None:
        if BANK_FILE.exists():
            _HELD = set(json.load(open(BANK_FILE))["probe_holdout"])
        else:
            _HELD = set()
    return _HELD


def core_held(core, pos):
    return f"{family_of(core)}|{norm_tid(core.tid)}|{atom_kind(core.lf)}|{pos}" in held()


def c2_held(which):
    return {"C2n": "C2|C2n|any|e", "C2f": "C2|C2f|any|e", "C2m": "C2|C2m|any|m"}[which] in held()


def enumerate_bank(n_cards=122, per=4):
    from . import build, gen
    from .plan import plan_cards
    cards = plan_cards(n_cards, seed_tag="bank")
    build.setup_cards(cards)
    by = collections.defaultdict(list)
    for c in cards:
        by[c["pair_index"]].append(c)
    T = {}
    for pi in sorted(by):
        for card in by[pi]:
            H = gen.H_for(card)
            rng = rng_for("bank", card["card_id"])
            for i in range(per * 3):
                s = {"i": i, "pair": None, "role": None, "v": rng.randrange(2), "g": rng.randrange(2),
                     "attack": False, "tag": rng.choice(["good", "bad"]), "vk": rng.randrange(4), "two_lcore": False}
                s.update(H.plan_slot(card, rng, s))
                ctx = dict(card)
                ctx.update(H.slot_ctx(card, s, rng))
                r = H.build_structure(ctx, s, rng)
                if r is None:
                    continue
                M, P, info = r
                for c in H.cores(ctx, M, P, rng, s).values():
                    if family_of(c) == "ID":
                        continue
                    for key in keys_of(c):
                        fam = key.split("|")[0]
                        T.setdefault(key, {"key": key, "family": fam, "core": norm_tid(c.tid), "position": key[-1],
                                           "atom": atom_kind(c.lf), "k": c.k, "lf_signature": sig(c.lf),
                                           "monotonicity": c.pol or "non-monotone/opaque", "lneg": list(c.lneg),
                                           "nd": c.nd, "side": "q", "example": c.matrix + "?" if key.endswith("|m")
                                           and c.matrix else c.clause})
    for k, ex in (("C2|C2n|any|e", "it is not the case that <P>"), ("C2|C2f|any|e", "it is false that <P>"),
                  ("C2|C2m|any|m", "Is it false that <P>?")):
        T[k] = {"key": k, "family": "C2", "core": k.split("|")[1], "position": k[-1], "atom": "any", "k": 1,
                "lf_signature": "NOT(<P>)", "monotonicity": "down", "lneg": ["it is not the case that" if "C2n" in k
                                                                             else "it is false that"], "nd": True,
                "side": "q", "example": ex}
    return T


def sig(lf):
    if not isinstance(lf, list):
        return "x"
    if lf[0] in ("not", "and", "or"):
        return lf[0].upper() + "(" + ",".join(sig(x) for x in lf[1:]) + ")"
    return lf[0]


ESSENTIAL = {"C1|C1.adj|adj|e", "C1|C1.has|has|e", "C1|C1.val|valid|e", "C1|C1.inv|inv|e", "C1|C1.st|stance|e",
             "C2|C2n|any|e", "C2|C2m|any|m", "C13|C13.neither|conn:adj|e", "C3|C3.failed|ev:renew|e",
             "C3|C3.failed|ev:renew|m", "C8|C8.notevery|q|e", "C8|C8.no|q|e", "C12|C12.mustnot|deon|e",
             "C13|C13.inv|conn:inv|e", "C6|C6.adj|adj|e"}


def draw_holdout(T, n=25, seed=SEED):
    """Stratified seeded draw: at most floor(1/3) of each family's templates, at least one from each of >= 10
    families (C4 text-only, C7 S5-only and essential N / D routes are not drawn)."""
    rng = random.Random(seed)
    fams = collections.defaultdict(list)
    for k, t in sorted(T.items()):
        if t["family"] in ("C7", "C4") or "+" in t["family"] or k in ESSENTIAL or t["k"] < 1:
            continue
        fams[t["family"]].append(k)
    cap = {f: len([k for k in T if T[k]["family"] == f]) // 3 for f in fams}
    order = sorted(fams)
    rng.shuffle(order)
    out = []
    for f in order:                     # one per family first
        if cap[f] >= 1 and fams[f]:
            out.append(rng.choice(fams[f]))
    pool = [(f, k) for f in fams for k in fams[f] if k not in out]
    rng.shuffle(pool)
    for f, k in pool:
        if len(out) >= n:
            break
        if sum(1 for x in out if T[x]["family"] == f) < cap[f]:
            out.append(k)
    return sorted(out[:n])


def main():
    T = enumerate_bank()
    hold = draw_holdout(T)
    fam_n = collections.Counter(t["family"] for t in T.values())
    doc = {"version": "F5 cue bank v1 (round 1)", "n_templates": len(T), "families": dict(sorted(fam_n.items())),
           "n_families": len(fam_n), "templates": sorted(T.values(), key=lambda t: t["key"]),
           "probe_holdout": hold, "probe_holdout_families": sorted({T[k]["family"] for k in hold})}
    s = json.dumps(doc, sort_keys=True)
    doc["sha256_of_templates_and_holdout"] = hashlib.sha256(s.encode()).hexdigest()
    json.dump(doc, open(BANK_FILE, "w"), indent=1)
    print(json.dumps({k: doc[k] for k in ("n_templates", "families", "n_families", "probe_holdout",
                                          "probe_holdout_families", "sha256_of_templates_and_holdout")}, indent=1))


if __name__ == "__main__":
    main()
