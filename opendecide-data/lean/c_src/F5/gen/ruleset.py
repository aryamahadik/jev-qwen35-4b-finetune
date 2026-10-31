"""Card rule sets (G0 3.1, SC10): no two F5 cards share a rule set, and two cards with the same sampler and world line
differ in their full key set or in a card constant beyond pack words. Each card in a (sampler, world, inverted) cell
gets a distinct combination of card constants, drawn by a seeded order and applied to the card:

  S1   n_vals of the declared value set (3-5), number of declared two-state (SEM-18) pairs (0-3), possession docs (0-2)
  S2   size of the declared status list (3-4), possession documents (1-3), risk events (1-2)
  S3   adjective predicates (4-6), declared two-state pairs (0-2), possession predicates (0-2)
  S4   graded-negative constant <q> (2-4), <m> (1-3), n_vals of the filter value set (3-5)
  INV  n_vals of the value set (3-4), flags per case (2-3), case outcome adjectives (4-6)
  S5   good adjectives (2-3), bad adjectives (2-3), size of the named party list (3-5)

The signature recorded per card is (sampler, world line, inverted, full key set, constants)."""
from __future__ import annotations

import itertools
import random

from .common import SEED


def knobs(card):
    s = card["sampler"]
    if card.get("inverted"):
        return [("nvals", (3, 4)), ("nflags", (2, 3)), ("nadj", (4, 5, 6))]
    if s == "S1":
        return [("nvals", (3, 4, 5)), ("naff", (0, 1, 2, 3)), ("ndocs", (0, 1, 2)), ("nqty", (2, 3, 1))]
    if s == "S2":
        return [("nstat", (3, 4)), ("ndocs", (1, 2, 3)), ("nrisk", (1, 2, 3))]
    if s == "S3":
        return [("nadj", (4, 5, 6)), ("naff", (0, 1, 2)), ("ndocs", (0, 1, 2))]
    if s == "S4":
        return [("q", (2, 3, 4)), ("m", (1, 2, 3)), ("nvals", (3, 4, 5))]
    if s == "S5":
        return [("ngood", (2, 3)), ("nbad", (2, 3)), ("nppl", (3, 4, 5))]
    return []


def apply(card, combo):
    """Apply a constants combination; returns False when the pack cannot support it."""
    s = card["sampler"]
    c = dict(combo)
    if card.get("inverted"):
        if card.get("cat") and len(card["cat"]["values"]) < c["nvals"]:
            return False
        if len(card["adjs"]) < c["nadj"] or c["nadj"] - 1 < c["nflags"]:
            return False
        if card.get("cat"):
            card["cat"] = {"name": card["cat"]["name"], "values": card["cat"]["values"][:c["nvals"]]}
        card["adjs"] = card["adjs"][:c["nadj"]]
        card["nflags"] = c["nflags"]
        card["ptags"] = {a["word"]: a["tag"] for a in card["adjs"]}
        return {a["tag"] for a in card["adjs"]} == {"good", "bad"}
    if s == "S1":
        if card["cats"]:
            if len(card["cats"][0]["values"]) < c["nvals"]:
                return False
            card["cats"] = [{"name": card["cats"][0]["name"], "values": card["cats"][0]["values"][:c["nvals"]]}]
        elif c["nvals"] != 3:
            return False
        withneg = [a for a in card["adjs"] if a.get("neg")]
        if len(withneg) < c["naff"]:
            return False
        keep = {a["word"] for a in withneg[:c["naff"]]}
        card["adjs"] = [a if a["word"] in keep else dict(a, neg=None) for a in card["adjs"]]
        card["negs"] = {a["word"]: a["neg"] for a in card["adjs"] if a.get("neg")}
        if card["fams"].get("C5"):
            if c["ndocs"] == 0 or len(card["docs"]) < c["ndocs"]:
                return False
            card["docs"] = card["docs"][:c["ndocs"]]
        elif c["ndocs"] != 0:
            return False
        if len(card["qtys"]) < c["nqty"]:
            return False
        card["qtys"] = card["qtys"][:c["nqty"]]
        card["tagged_qtys"] = [q for q in card["qtys"] if q.get("tag")]
        return True
    if s == "S2":
        if len(card["statuses"]) < c["nstat"] or len(card["docs"]) < c["ndocs"] or len(card["risks"]) < c["nrisk"]:
            return False
        card["statuses"] = card["statuses"][:c["nstat"]]
        card["docs"] = card["docs"][:c["ndocs"]]
        card["doc_tags"] = {d: card["doc_tags"].get(d, "good") for d in card["docs"]}
        card["risks"] = card["risks"][:c["nrisk"]]
        return True
    if s == "S3":
        if len(card["adjs"]) < c["nadj"]:
            return False
        adjs = card["adjs"][:c["nadj"]]
        if {a["tag"] for a in adjs} != {"good", "bad"}:
            return False
        withneg = [a for a in adjs if a.get("neg")]
        if len(withneg) < c["naff"]:
            return False
        keep = {a["word"] for a in withneg[:c["naff"]]}
        adjs = [a if a["word"] in keep else dict(a, neg=None) for a in adjs]
        if card["fams"].get("C5"):
            if c["ndocs"] == 0 or len(card["docs"]) < c["ndocs"]:
                return False
            docs = card["docs"][:c["ndocs"]]
        else:
            if c["ndocs"] != 0:
                return False
            docs = []
        card["adjs"], card["docs"] = adjs, docs
        card["negs"] = {a["word"]: a["neg"] for a in adjs if a.get("neg")}
        tags = {f"has:{d}": card["ptags"].get(f"has:{d}", "good") for d in docs}
        card["preds"] = [f"adj:{a['word']}" for a in adjs] + [f"has:{d}" for d in docs]
        card["ptags"] = {f"adj:{a['word']}": a["tag"] for a in adjs} | tags
        return True
    if s == "S4":
        if len(card["cat"]["values"]) < c["nvals"]:
            return False
        card["cat"] = {"name": card["cat"]["name"], "values": card["cat"]["values"][:c["nvals"]]}
        card["q_graded"] = c["q"]
        card["m_graded"] = c["m"]
        return True
    if s == "S5":
        good = [a for a in card["adjs"] if a["tag"] == "good"]
        bad = [a for a in card["adjs"] if a["tag"] == "bad"]
        if len(good) < c["ngood"] or len(bad) < c["nbad"] or len(card["people"]) < c["nppl"]:
            return False
        card["adjs"] = good[:c["ngood"]] + bad[:c["nbad"]]
        card["ptags"] = {a["word"]: a["tag"] for a in card["adjs"]}
        card["people"] = list(card["people"])[:c["nppl"]]
        return True
    return True


def signature(c):
    from . import gen
    H = gen.H_for(c)
    return [c["sampler"], c["world"], bool(c.get("inverted")), sorted(H.full_keys(c)), c.get("constants")]


def assign(cards, tag="r1"):
    """Distinct rule-set signatures: each card (most constrained first) takes the first feasible constants combination
    whose signature (sampler, world, inverted, full key set, constants) no other card holds."""
    rng = random.Random(f"{SEED}-rules-{tag}")
    REF = ("partner", "pack")       # shared objects: never copied (the partner must stay the live card)

    def cp(d):
        return {k: (v.copy() if isinstance(v, (dict, list)) and k not in REF else v) for k, v in d.items()}
    snaps = {c["card_id"]: cp(c) for c in cards}
    feas = {}
    for c in cards:
        ks = knobs(c)
        combos = list(itertools.product(*[v for _, v in ks]))
        rng.shuffle(combos)
        ok = []
        for combo in combos:
            trial = cp(snaps[c["card_id"]])
            if apply(trial, list(zip([n for n, _ in ks], combo))):
                ok.append(combo)
        feas[c["card_id"]] = (ks, ok)
    used = set()
    clashes = 0
    for c in sorted(cards, key=lambda c: (len(feas[c["card_id"]][1]), c["card_id"])):
        ks, ok = feas[c["card_id"]]
        done = False
        for combo in ok:
            trial = cp(snaps[c["card_id"]])
            apply(trial, list(zip([n for n, _ in ks], combo)))
            trial["constants"] = dict(zip([n for n, _ in ks], combo))
            sg = str(signature(trial))
            if sg in used:
                continue
            c.update(trial)
            used.add(sg)
            done = True
            break
        if not done:
            clashes += 1
            if ok:
                apply(c, list(zip([n for n, _ in ks], ok[0])))
                c["constants"] = dict(zip([n for n, _ in ks], ok[0]))
            else:
                c["constants"] = None
    sigs = {c["card_id"]: signature(c) for c in cards}
    dup = len(sigs) - len({str(v) for v in sigs.values()})
    return sigs, clashes, dup
