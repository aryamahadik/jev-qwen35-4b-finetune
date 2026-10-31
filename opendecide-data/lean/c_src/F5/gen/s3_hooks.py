"""S3 hooks: fact-graph bases, cue cores (identity, C1, C5, C6, C13, C16, C8 group scope, C11 other than)."""
from __future__ import annotations

import random

from . import s3
from .forms import Core, NOT, adj_cores, conn_cores, has_cores

SAMPLER = "S3"


def card_setup(card):
    pv = card["pack"]
    rng = random.Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 12]
    card["ent"] = rng.choice(ents)
    good = [a for a in pv["adjs"] if a["tag"] == "good"]
    bad = [a for a in pv["adjs"] if a["tag"] == "bad"]
    rng.shuffle(good)
    rng.shuffle(bad)
    adjs = good[:3] + bad[:3]
    if not card["fams"].get("C6"):
        adjs = [dict(a, neg=None) for a in adjs]
    card["adjs"] = adjs
    card["negs"] = {a["word"]: a["neg"] for a in adjs if a.get("neg")}
    docs = [d for d in pv["docs"] if d != card["ent"]["noun"]]
    rng.shuffle(docs)
    card["docs"] = docs[:2] if card["fams"].get("C5") else []
    card["preds"] = [f"adj:{a['word']}" for a in adjs] + [f"has:{d}" for d in card["docs"]]
    card["ptags"] = {f"adj:{a['word']}": a["tag"] for a in adjs}
    card["ptags"].update({f"has:{d}": pv["doc_tags"].get(d, "good") for d in card["docs"]})
    card["inert"] = [x for x in pv.get("inert", []) if len(x) < 120]
    return card


def plan_slot(card, rng, s):
    depth = rng.choices([1, 2, 3], [56, 41, 3])[0]
    if s["vk"] == 0 and not card["fams"].get("C16"):
        s["vk"] = 1
    return {"kind": "fact", "depth": depth}


def slot_ctx(card, slot, rng):
    pool = [p for p, t in card["ptags"].items() if t == slot["tag"]]
    return {"base_pred": rng.choice(pool)}


def solve(M, lfs):
    return s3.solve_a(M, lfs)


def build_structure(card, slot, rng):
    M, E = s3.sample(rng, card, card["world"], slot["depth"], slot["v"], card["base_pred"])
    try:
        val, layer = s3.solve(M)
    except ValueError:
        return None
    if len(s3.ground(M)) > 18:
        return None
    kind, w = card["base_pred"].split(":", 1)
    P = [kind, s3.subj(M, E), w]
    try:
        (v,) = s3.solve_a(M, [P])
    except ValueError:
        return None
    d = layer.get((E, card["base_pred"]))
    if d is None:
        d = slot["depth"]
    if d != slot["depth"]:
        return None
    M["base_e"] = E
    return M, P, {"depth": d}


def cores(card, M, P, rng, slot):
    out = {}
    subj = P[1]
    E = M["base_e"]
    kind, w = P[0], P[2]
    if kind == "adj":
        for c in adj_cores(subj, w, M["negs"].get(w)):
            out[c.tid] = c
        for p in M["preds"]:
            k2, w2 = p.split(":", 1)
            if k2 == "adj" and w2 != w:
                for c in conn_cores(subj, w, w2):
                    c.tid = f"{c.tid}:{w2}"
                    out[c.tid] = c
    else:
        for c in has_cores(subj, w):
            out[c.tid] = c
    vp = f"is {w}" if kind == "adj" else f"has a {w}"
    vpm = f"is any {M['noun']} other than {subj} {w}" if kind == "adj" else \
        f"does any {M['noun']} other than {subj} have a {w}"
    pred = [kind, w]
    grp = M["noun"]
    tag = card["ptags"][f"{kind}:{w}"]
    out["C8.notevery"] = Core("C8.notevery", ("C8",), f"not every {grp} in this record {vp}", None,
                              NOT(["grp", "every", grp, pred, None]), 1, "down", lneg=("not every",), rel="other",
                              ptag=tag)
    out["C8.no"] = Core("C8.no", ("C8",), f"no {grp} in this record {vp}", None,
                        NOT(["grp", "some", grp, pred, None]), 1, "down", lneg=("no",), rel="other", ptag=tag)
    out["C11.other"] = Core("C11.other", ("C11",), f"some {grp} in this record other than {subj} {vp}",
                            f"Among the {M['plural']} in this record, {vpm}", ["grp", "some", grp, pred, E], 1, "up",
                            lneg=("other than",), rel="other", ptag=tag)
    return out


def is_v_core(card, c):
    if not c.fam or not all(card["fams"].get(f, False) for f in c.fam):
        return False
    if c.rel in ("conn", "other"):
        return True
    return c.fam in (("C6",), ("C5",)) and c.k == 1


def nd_ok(card, c):
    return all(card["fams"].get(f, False) for f in c.fam)


def valid_structure(card, M, P):
    try:
        s3.solve(M)
    except ValueError:
        return False
    return len(s3.ground(M)) <= 18


def tag_of(card, P, M):
    return card["ptags"].get(f"{P[0]}:{P[2]}")


def perturb(M, rng):
    return s3.perturb(M, rng)


def doc(M, inert=None, attack=None):
    return s3.doc_ir(M, attack=attack)


def text_triggers(M):
    keys = {"SEM-01", "SEM-02" if M["world"] == "closed" else "SEM-03", "SEM-22"}
    if M.get("decoy_text"):
        keys.add("SEM-28")
    if any(f["form"] == "aff" for f in M["facts"]):
        keys.add("SEM-18")
    if any(f["form"] == "lacks" for f in M["facts"]):
        keys.add("SEM-19")
    return keys


def full_keys(card):
    keys = {"SEM-01", "SEM-02" if card["world"] == "closed" else "SEM-03", "SEM-22"}
    if card["negs"]:
        keys.add("SEM-18")
    if card["docs"]:
        keys.add("SEM-19")
    if card["fams"].get("C13"):
        keys.add("SEM-10")
    keys.add("SEM-28")
    if card["fams"].get("C11"):
        keys.add("SEM-23")
    return keys


def sem_params(card, M):
    return {"etype": card["ent"]["noun"], "affixed": sorted(card["negs"].items()), "value_sets": []}


def affixed_used(M):
    return sorted(set(M["negs"].values()))


def t_txt(M):
    from .common import negc
    sents = [s3.univ_text(M, u) for u in M["univ"]] + [s3.lit_text(M, f["e"], f["p"], f["val"], f["form"])
                                                      for f in M["facts"] if f["form"] != "decoy"]
    if M.get("decoy_text"):
        sents.append("not only")
    aff = affixed_used(M)
    return sum(1 for x in sents if negc(x, aff).k_all > 0)


def fewshot(card, b):
    M = b["M"]
    n = card["ent"]["noun"]
    ids = [x for x in card["ent"]["ids"] if x not in M["ents"]]
    w = [p.split(":", 1)[1] for p in card["preds"] if p.startswith("adj:")]
    return [{"case": f"Statements: Every {n} that is {w[0]} is {w[1]}. {s3.cap(n)} {ids[0]} is {w[0]}. "
                     f"Question: Is it true that {n} {ids[0]} is not {w[1]}?", "answer": "No"},
            {"case": f"Statements: No {n} that is {w[0]} is {w[-1]}. {s3.cap(n)} {ids[1]} is {w[0]}. "
                     f"Question: Is it false that {n} {ids[1]} is {w[-1]}?", "answer": "Yes"}]


def inverted_block(card, b):
    return None


T_BUCKETS = {"0-1": 0.35, "2": 0.3, "3": 0.2, "4+": 0.15}


def t_bucket(M):
    t = t_txt(M)
    if t == 0 and M["world"] == "open":
        # repair r2 (G10 negation-location cell "none"): an open card decides No only through a stated negative fact,
        # so a v(P) = 0 open base always has text-side negation; open bases with none (t = 0) are never drawn, so
        # the presence of text-side negation says nothing about the label (bucket "0-1" means t = 1 on open cards)
        return "0"
    return "0-1" if t <= 1 else ("4+" if t >= 4 else str(t))
