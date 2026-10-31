"""S1 hooks for the base builder: card constants, slot plans, structures meeting the slot targets, cue cores."""
from __future__ import annotations

from . import s1
from .forms import Core, adj_cores, amt_cores, conn_cores, deon_cores

SAMPLER = "S1"


def card_setup(card):
    pv = card["pack"]
    rng = __import__("random").Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 12]
    card["ent"] = rng.choice(ents)
    good = [a for a in pv["adjs"] if a["tag"] == "good"]
    bad = [a for a in pv["adjs"] if a["tag"] == "bad"]
    rng.shuffle(good)
    rng.shuffle(bad)
    card["adjs"] = good[:4] + bad[:4]
    card["negs"] = {a["word"]: a["neg"] for a in card["adjs"] if a.get("neg")}
    if not card["fams"].get("C6"):
        card["negs"] = {}
        card["adjs"] = [dict(a, neg=None) for a in card["adjs"]]
    docs = list(pv["docs"])
    rng.shuffle(docs)
    card["docs"] = docs[:2] if card["fams"].get("C5") else []
    qs = list(pv["qtys"])
    rng.shuffle(qs)
    card["qtys"] = qs[:3]
    card["tagged_qtys"] = [q for q in card["qtys"] if q.get("tag")]
    cats = list(pv["cats"])
    rng.shuffle(cats)
    card["cats"] = cats[:1]
    # repair r2 (G10 SEM-key cell): the deontic layer (SEM-24 on the card) is on for both cards of an antithetic pair
    # or for neither, so the SEM-24 rows are seen at r and 1 - r
    pvs = [pv] + ([card["partner"]["pack"]] if card.get("partner") else [])
    card["deontic"] = bool(card["fams"].get("C12")) and all(len(p["actions"]) >= 2 and len(p["roles"]) >= 2
                                                            for p in pvs)
    card["roles"] = pv["roles"][:3]
    card["actions_full"] = [a for a in pv["actions"] if a["effect"] in ("favourable", "protective")][:4]
    card["actions"] = [a["verb"] for a in pv["actions"]][:4]
    card["deon_base"] = card["deontic"] and any(a["effect"] == "favourable" for a in card["actions_full"]) and \
        any(a["effect"] == "protective" for a in card["actions_full"])
    return card


def plan_slot(card, rng, s):
    kinds, w = ["out"], [60]
    pc = card["partner"]
    if card["tagged_qtys"] and pc["tagged_qtys"] and card["fams"].get("C9"):
        kinds.append("amt")
        w.append(25)
    if card.get("deon_base") and pc.get("deon_base") and s["vk"] >= 1:
        kinds.append("deon")
        w.append(15)
    kind = rng.choices(kinds, w)[0]
    if kind == "out" and s["vk"] == 0 and not card["fams"].get("C16"):
        s["vk"] = 1
    if kind == "out":
        depth = rng.choices([1, 2, 3], [55, 42, 3])[0]
    else:
        depth = 1
    return {"kind": kind, "depth": depth, "which": rng.choice(["perm", "req"])}


def slot_ctx(card, slot, rng):
    kind = slot["kind"]
    ctx = {}
    if kind == "out":
        pool = [a["word"] for a in card["adjs"] if a["tag"] == slot["tag"]]
        ctx["slot_out"] = rng.choice(pool)
    elif kind == "amt":
        ctx["slot_qty"] = rng.choice(card["tagged_qtys"])
        ctx["slot_out"] = None
    elif kind == "deon":
        eff = "favourable" if slot["tag"] == "good" else "protective"
        acts = [a["verb"] for a in card["actions_full"] if a["effect"] == eff]
        ctx["slot_action"] = rng.choice(acts)
        ctx["slot_role"] = rng.choice(card["roles"])
        ctx["slot_out"] = None
    return ctx


def solve(M, lfs):
    return s1.solve_a(M, lfs)


def build_structure(card, slot, rng):
    kind = slot["kind"]
    depth = slot["depth"]
    card = dict(card, pairmode=slot.get("pair") is not None and rng.random() < 0.8)
    M = s1.sample_structure(rng, card, kind, depth, card["world"])
    subj = M["subj"]
    if kind == "out":
        P = ["adj", subj, card["slot_out"]]
        d = s1.depth_of(M, card["slot_out"])
    elif kind == "deon":
        P = ["deon", slot["which"], card["slot_role"], card["slot_action"], f"the {M['noun']}"]
        if not any(r["head"]["kind"] == "deon" and r["head"]["role"] == card["slot_role"] and
                   r["head"]["verb"] == card["slot_action"] for r in M["rules"]):
            return None
        d = s1.deon_depth(M, card["slot_role"], card["slot_action"])
    else:
        a = M["amount"]
        if a is None:
            return None
        v0 = M["nums"][a["qty"]]
        if not isinstance(v0, int):
            return None
        amt = min(v0, a["limit"]) if a["kind"] == "cap" else max(v0, a["limit"])
        qt = card["slot_qty"]["tag"]
        up = (slot["tag"] == "bad") == (qt == "high_bad")
        op = rng.choice([">=", ">"] if up else ["<=", "<"])
        step = card["slot_qty"]["step"]
        n = amt if rng.random() < 0.3 else amt + rng.choice([-step, step])
        if n <= 0:
            return None
        P = ["amt", a["name"], subj, op, n]
        d = 1
    if d != depth or len(M["rules"]) < 2:
        return None
    if kind == "out" and not any(r["head"]["kind"] == "adj" and r["head"]["word"] == P[2] for r in M["rules"]):
        return None
    try:
        s1.solve_a(M, [P])
    except (s1.Unknown, s1.Inconsistent, KeyError):
        return None
    if rng.random() < 0.5:
        s1_add_decoy(M, rng)
    return M, P, {"depth": d}


def s1_add_decoy(M, rng):
    tr = [k[4:] for k, x in M["facts"].items() if k.startswith("adj:") and x is True]
    if len(tr) < 2:
        return False
    a, b = rng.sample(sorted(tr), 2)
    M["decoy_text"] = [a, b]
    M["fact_form"]["adj:" + a] = "omit"
    M["fact_form"]["adj:" + b] = "omit"
    return True


def cores(card, M, P, rng, slot):
    subj = M["subj"]
    out = {}
    if P[0] == "adj":
        w = P[2]
        for c in adj_cores(subj, w, M["negs"].get(w)):
            out[c.tid] = c
        cands = [o for o in M["outs"] if o != w] + sorted(k[4:] for k in M["facts"] if k.startswith("adj:"))
        for b in cands:
            if b == w:
                continue
            for c in conn_cores(subj, w, b):
                c.tid = f"{c.tid}:{b}"
                out[c.tid] = c
    elif P[0] == "deon":
        for c in deon_cores(P[2], P[3], P[4], P[1]):
            out[c.tid] = c
    elif P[0] == "amt":
        name, op, n = P[1], P[3], P[4]
        unit = M["units"][M["amount"]["qty"]]
        pick = int(rng.random() * 3)
        for c in amt_cores(name, subj, op, n, unit, pick):
            out[c.tid] = c
        step = 1
        for q in card["qtys"]:
            if q["name"] == M["amount"]["qty"]:
                step = q["step"]
        eq = {">=": ("not less than", ">=", n), "<=": ("not more than", "<=", n),
              ">": ("not less than", ">=", n + step), "<": ("not more than", "<=", n - step)}[op]
        neq = {">=": ("not more than", "<=", n - step), "<=": ("not less than", ">=", n + step),
               ">": ("not more than", "<=", n), "<": ("not less than", ">=", n)}[op]
        for tag, (ph, o2, n2), pol in (("eq", eq, "up"), ("neq", neq, "down")):
            if n2 <= 0:
                continue
            text = f"the {name} of {subj} is {ph} {n2} {unit}"
            out[f"C9.negcmp.{tag}"] = Core(f"C9.negcmp.{tag}", ("C9",), text, None, ["amt", name, subj, o2, n2], 1,
                                           pol, lneg=(ph,), rel="negcmp")
    if card.get("deontic") and P[0] != "deon":
        pairs = sorted({(r["head"]["role"], r["head"]["verb"]) for r in M["rules"] if r["head"]["kind"] == "deon"})
        for role, verb in pairs:
            for which in ("perm", "req"):
                eff = next((a["effect"] for a in card["actions_full"] if a["verb"] == verb), None)
                ptag = {"favourable": "good", "protective": "bad"}.get(eff)
                if ptag is None:
                    continue
                for c in deon_cores(role, verb, f"the {M['noun']}", which):
                    if c.fam == ("C12",):
                        c.tid = f"{c.tid}:{role}:{verb}"
                        c.rel = "other"
                        c.ptag = ptag
                        out[c.tid] = c
    return out


def is_v_core(card, c):
    if not c.fam or not all(card["fams"].get(f, False) for f in c.fam):
        return False
    return c.fam in (("C13",), ("C16",), ("C12",), ("C9",))


def nd_ok(card, c):
    return all(card["fams"].get(f, False) for f in c.fam)


def valid_structure(card, M, P):
    return True


def tag_of(card, P, M):
    if P[0] == "adj":
        return next((a["tag"] for a in card["adjs"] if a["word"] == P[2]), None)
    if P[0] == "deon":
        eff = next((a["effect"] for a in card["actions_full"] if a["verb"] == P[3]), None)
        return {"favourable": "good", "protective": "bad"}.get(eff)
    if P[0] == "amt":
        t = card["slot_qty"].get("tag")
        up = P[3] in (">=", ">")
        if t == "high_bad":
            return "bad" if up else "good"
        if t == "low_bad":
            return "good" if up else "bad"
    return None


def perturb(M, rng):
    keep = set(M.get("decoy_text") or [])
    return [(d, m) for d, m in s1.perturb_fact(M, rng) if not any(d == f"fact adj:{w} -> False" for w in keep)]


def doc(M, inert=None, attack=None):
    return s1.doc_ir(M, inert=inert, attack=attack)


def text_triggers(M):
    """SEM keys fired by program-written text (generator side; the card parser recomputes them from the text)."""
    keys = {"SEM-01", "SEM-02" if M["world"] == "closed" else "SEM-03"}
    keys |= s1.mentions(M)
    lits = []
    for r in M["rules"]:
        lits += r["conds"] + ([r["exc"]] if r.get("exc") else [])
        if r["head"]["kind"] == "adj" and r["head"]["pol"] == "aff":
            keys.add("SEM-18")
    if any(l["t"] == "num" for l in lits) or M.get("amount"):
        keys |= {"SEM-08", "SEM-12", "SEM-14"}
    if any(isinstance(x, int) for x in M["nums"].values()):
        keys |= {"SEM-12", "SEM-14"}
    if any(x == "NR" for x in list(M["nums"].values()) + list(M["cats"].values())):
        keys.add("SEM-04")
    if M["cats"]:
        keys.add("SEM-17")
    if any(l["t"] in ("adj", "out") and l["pol"] == "aff" for l in lits) or \
            any(f == "aff" for f in M["fact_form"].values()):
        keys.add("SEM-18")
    if any(l["t"] == "has" and l["pol"] == "lacks" for l in lits) or \
            any(f == "lacks" for f in M["fact_form"].values()):
        keys.add("SEM-19")
    if M.get("decoy_text"):
        keys.add("SEM-28")
    return keys


def full_keys(card):
    keys = {"SEM-01", "SEM-02" if card["world"] == "closed" else "SEM-03", "SEM-05", "SEM-06", "SEM-07", "SEM-15",
            "SEM-08", "SEM-12", "SEM-14", "SEM-28"}
    if card["world"] == "closed":
        keys.add("SEM-04")
    if card["cats"]:
        keys.add("SEM-17")
    if card["negs"]:
        keys.add("SEM-18")
    if card["docs"]:
        keys.add("SEM-19")
    if card["fams"].get("C13"):
        keys.add("SEM-10")
    if card.get("deontic"):
        keys.add("SEM-24")
    return keys


def sem_params(card, M):
    """Placeholder values for the SEM lines of this base's card."""
    p = {"etype": card["ent"]["noun"]}
    p["value_sets"] = [(c["name"], c["values"]) for c in card["cats"]]
    p["affixed"] = sorted(card["negs"].items())
    return p


def affixed_used(M):
    return sorted(set(M["negs"].values()))


def t_txt(M):
    """Text-side cue instances that carry an L_neg entry (rule, fact and amount sentences; decisive or not)."""
    from .common import negc
    sents = [s1.rule_text(r, M) for r in M["rules"]] + s1.fact_sentences(M)
    if M.get("amount"):
        sents.append(s1.amount_text(M))
    aff = affixed_used(M)
    return sum(1 for x in sents if negc(x, aff).k_all > 0)


def fewshot(card, b):
    """1-2 worked examples on other entities of the pack (never the row's base): modus ponens and only-if, labels
    the same in both worlds."""
    ids = [x for x in card["ent"]["ids"] if x not in b["M"]["subj"]]
    n = card["ent"]["noun"]
    adjs = [a["word"] for a in card["adjs"]]
    w1, o1, w2, o2 = adjs[0], adjs[1], adjs[2 % len(adjs)], adjs[3 % len(adjs)]
    s2, s3 = f"{n} {ids[0]}", f"{n} {ids[1]}"
    return [{"case": f"Rule: If the {n} is {w1}, then the {n} is {o1}. Fact: {s1.cap(s2)} is {w1}. "
                     f"Question: Is it true that {s2} is not {o1}?", "answer": "No"},
            {"case": f"Rule: The {n} is {o2} only if the {n} is {w2}. Fact: {s1.cap(s3)} is not {w2}. "
                     f"Question: Is it false that {s3} is {o2}?", "answer": "Yes"}]


def inverted_block(card, b):
    return None


T_BUCKETS = {"0-1": 0.17, "2": 0.2, "3": 0.2, "4+": 0.43}


def t_bucket(M):
    t = t_txt(M)
    return "0-1" if t <= 1 else ("4+" if t >= 4 else str(t))
