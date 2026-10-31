"""S7 real-text codebook variants (spec 2.3; G0 section 3 S7). Codebooks and records come from formats-2 (step-4
artifacts); EDOS stays out (register row 17 does not list the per-annotator file: X15 gate, R5-F). Records: train
part of the shared split file only, minus every text equal to a dev-part text, minus public-3 claims; one claim per
normalized text across F10 S7 groups and examples. Gold = the program map of the human annotation (first fit)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from functools import lru_cache

import lexicon as L
from common import CSRC, FMT2_DIR, uhash

DATASETS = {"xed": "xed", "mams_acsa": "mams_acsa", "mams_atsa": "mams_atsa", "ghc": "ghc"}
REC_FILE = {"xed": "xed.jsonl", "mams_acsa": "mams_acsa.jsonl", "mams_atsa": "mams_atsa.jsonl", "ghc": "ghc.jsonl"}


@lru_cache(maxsize=1)
def lexicons():
    lx = json.load(open(FMT2_DIR / "codebooks" / "lexicon.json"))
    return {x["scheme"]: x for x in lx["lexicons"]}


@lru_cache(maxsize=1)
def codebooks():
    out = []
    for l in open(FMT2_DIR / "codebooks" / "codebooks.jsonl"):
        c = json.loads(l)
        if c["family"] == "F10" and c["status"] == "ready" and c["scheme"] in DATASETS:
            out.append(c)
    return out


@lru_cache(maxsize=1)
def split_info():
    dev, part = set(), {}
    for l in open(CSRC / "public" / "public-3" / "out" / "public3_split_3e.jsonl"):
        r = json.loads(l)
        part[r["id"]] = r["part"]
        if r["part"] != "train":
            dev.add(r["norm_sha256"])
    claimed = set()
    for l in open(CSRC / "public" / "public-3" / "out" / "public3_record_claims.jsonl"):
        claimed.add(json.loads(l)["norm_sha256"])
    return part, dev, claimed


@lru_cache(maxsize=4)
def records(scheme):
    """Eligible records (F10_S7 flag) after dev separation and public claims; counts of every drop."""
    part, dev, claimed = split_info()
    drops = Counter()
    out = []
    for l in open(FMT2_DIR / "records" / REC_FILE[scheme]):
        r = json.loads(l)
        if not (r.get("eligible") or {}).get("F10_S7"):
            drops["not_eligible"] += 1
            continue
        if part.get(r["id"], "train") != "train":
            drops["dev_part"] += 1
            continue
        if r["norm_sha256"] in dev:
            drops["dev_text"] += 1
            continue
        if r["norm_sha256"] in claimed:
            drops["public_claim"] += 1
            continue
        out.append(r)
    return out, dict(drops)


# ------------------------------------------------------------------------------------------------ semantics
def units(rec, scheme):
    """Coding units of a record: one per record, or one per eligible asked target on ATSA (target uniqueness)."""
    if scheme != "mams_atsa":
        return [(rec, None)]
    terms = rec["ann"]["terms"]
    if not rec["ann"].get("terms_unique", False):
        return []
    txt = rec["text"].lower()
    out = []
    for i, t in enumerate(terms):
        if txt.count(t["term"].lower()) == 1 and t.get("span_ok", True):
            out.append((rec, i))
    return out


def lit(atom, rec, ti, scheme):
    a = rec["ann"]
    k = atom[0]
    if k == "EMO":
        em = set(a["emotions"])
        return em == {"neutral"} if atom[1] == "neutral" else atom[1] in em
    if k == "PAIR":
        return [atom[1], atom[2]] in [list(x) for x in a["aspects"]]
    if k == "CAT":
        return atom[1] in {x[0] for x in a["aspects"]}
    if k == "POL":
        return atom[1] in {x[1] for x in a["aspects"]}
    if k == "TPOL":
        return a["terms"][ti]["polarity"] == atom[1]
    if k == "OTHER":
        return atom[1] in {t["polarity"] for j, t in enumerate(a["terms"]) if j != ti}
    if k == "FLAG":
        return int(a.get(atom[1], 0)) == 1
    raise ValueError(k)


def cond(c, rec, ti, scheme):
    op = c["op"]
    if op == "LIT":
        return lit(c["atom"], rec, ti, scheme) != c["neg"]
    if op == "ALL":
        return all(cond(x, rec, ti, scheme) for x in c["args"])
    if op == "ANY":
        return any(cond(x, rec, ti, scheme) for x in c["args"])
    if op == "RESIDUAL":
        return False
    raise ValueError(op)


def first_fit(codes, rec, ti, scheme):
    for i, c in enumerate(codes):
        if c["residual"]:
            return i
        if cond(c["condition"], rec, ti, scheme):
            return i
    return len(codes) - 1


def fits(code, rec, ti, scheme):
    return cond(code["condition"], rec, ti, scheme) if not code["residual"] else None


# ------------------------------------------------------------------------------------------------ rendering
def _tpls(lex, form):
    return [t["template"] for t in lex["templates"] if t["form"] == form]


def lit_text(atom, neg, lex, key):
    k = atom[0]
    names = lex.get("names") or {}
    if k == "EMO":
        if atom[1] == "neutral":
            t = _tpls(lex, "EMO-neutral" if neg else "EMO+neutral")
            return t[int(uhash(key) * len(t)) % len(t)]
        t = _tpls(lex, "EMO-" if neg else "EMO+")
        return t[int(uhash(key) * len(t)) % len(t)].format(v=atom[1])
    if k in ("PAIR", "CAT", "POL", "TPOL", "OTHER", "FLAG"):
        t = _tpls(lex, k + ("-" if neg else "+"))
        tpl = t[int(uhash(key) * len(t)) % len(t)]
        if k == "PAIR":
            return tpl.format(c=atom[1], p=atom[2])
        if k == "CAT":
            return tpl.format(c=atom[1])
        if k == "FLAG":
            return tpl.format(f=names.get(atom[1], atom[1]))
        return tpl.format(p=atom[1])
    raise ValueError(k)


def cond_text(c, lex, key):
    op = c["op"]
    if op == "LIT":
        return lit_text(c["atom"], c["neg"], lex, key)
    head = L.LIST_HEAD["ALL" if op == "ALL" else "ANY"]
    return head + ": " + L.ITEM_SEP.join(cond_text(x, lex, key + (i,)) for i, x in enumerate(c["args"]))


def code_line(card, i):
    c = card["codes"][i]
    nm = card["qnames"][i]
    if c["residual"]:
        return f"{nm}: {L.ST['ST45'][card['resid_i']]}."
    return f"{nm}: {cond_text(c['condition'], card['lex'], (card['card_id'], i))}."


def card_ir(card):
    lines = [code_line(card, i) for i in range(len(card["codes"]))]
    ex = [L.EXAMPLE_FRAME.format(X=L.EXAMPLE_S7.format(R=e["text"], T=card["qnames"][e["code"]]))
          for e in card.get("examples", [])]
    blocks = [{"type": "para", "text": card["intro"]}, {"type": "items", "items": lines}]
    if ex:
        blocks.append({"type": "items", "items": ex})
    blocks.append({"type": "items", "items": card["rule_text"]})
    return {"blocks": blocks}

NEG_EMO = {"anger", "disgust", "fear", "sadness"}
POS_EMO = {"joy", "trust"}
LICENCE = {"xed": "CC BY 4.0 (XED, Helsinki-NLP; register section 6)", "mams_acsa": "Apache-2.0 (MAMS)",
           "mams_atsa": "Apache-2.0 (MAMS)", "ghc": "CC BY 4.0 (Gab Hate Corpus)"}


def _poslits(c, out):
    if c["op"] == "LIT":
        out.append((c["atom"], c["neg"]))
    for x in c.get("args", []) or []:
        _poslits(x, out)
    return out


def code_polarity(code, r):
    if code["residual"]:
        return None
    lits = _poslits(code["condition"], [])
    for atom, neg in lits:
        if neg:
            continue
        k = atom[0]
        if k == "FLAG":
            return "bad"
        if k in ("PAIR", "POL", "TPOL", "OTHER"):
            p = atom[-1]
            if p == "negative":
                return "bad"
            if p == "positive":
                return "not bad"
        if k == "EMO":
            if atom[1] in NEG_EMO:
                return "bad"
            if atom[1] in POS_EMO:
                return "not bad"
    if lits and all(neg for _, neg in lits) and lits[0][0][0] == "FLAG":
        return "not bad"
    return None


def build_s7_card(cb, idx, mode, r, ex_on):
    from cardgen import neutral_ids
    scheme = cb["scheme"]
    codes = cb["codes"]
    n = len(codes)
    card = {"card_id": f"F10-S7-{idx:02d}", "sampler": "S7", "ctype": "codebook", "scheme": scheme,
            "dataset": cb["dataset"], "codebook_id": cb["id"], "codes": codes, "lex": lexicons()[scheme],
            "mode": mode, "world": None, "entity": "text"}
    nonres = [i for i, c in enumerate(codes) if not c["residual"]]
    if mode == "natural":
        names = [c["natural_name"] for c in codes]
    elif mode == "neutral":
        names = neutral_ids(r, n)
    else:
        nat = [codes[i]["natural_name"] for i in nonres]
        for _ in range(50):
            perm = nat[:]
            r.shuffle(perm)
            if all(a != b for a, b in zip(perm, nat)):
                break
        names = [None] * n
        for i, nm in zip(nonres, perm):
            names[i] = nm
        for i, c in enumerate(codes):
            if c["residual"]:
                names[i] = c["natural_name"]
    q = r.choice(L.QUOTE_FORMS)
    card["names"] = names
    card["qform"] = q
    card["qnames"] = [q.format(n=x) for x in names]
    card["resid_i"] = int(uhash(card["card_id"], "resid") * len(L.ST["ST45"]))
    card["intro"] = f"This codebook codes the {cb['dimension']}."
    pol = {}
    undecided = []
    for i in nonres:
        p = code_polarity(codes[i], r)
        if p is None:
            undecided.append(i)
        pol[i] = p
    tags = ["bad", "not bad"] * (len(undecided) // 2 + 1)
    r.shuffle(tags)
    for i, t in zip(undecided, tags):
        pol[i] = t
    card["polarity"] = pol
    rid = ["ST1_S7", "ST2", "ST33_S7", "ST44"]
    if scheme == "mams_atsa":
        rid.append("ST46")
    if scheme == "mams_acsa":
        rid.append("ST47")
    if mode == "neutral":
        rid.append("ST36")
    card["ex_on"] = ex_on and n <= 9
    if card["ex_on"]:
        rid.append("ST37_S7")
    off = idx
    card["rules"] = [(i, (off + int(uhash("rr", i) * 1000)) % len(L.ST[i])) for i in rid]
    card["rule_text"] = [L.ST[i][j] for i, j in card["rules"]]
    return card


class Pool7:
    """Unclaimed units of one scheme indexed by first-fit code of one codebook; one claim per normalized text."""

    def __init__(self, scheme, claimed: set):
        self.scheme = scheme
        self.recs, self.drops = records(scheme)
        self.claimed = claimed
        self.units = [u for rec in self.recs for u in units(rec, scheme)]

    def index(self, codes):
        idx = defaultdict(list)
        for rec, ti in self.units:
            idx[first_fit(codes, rec, ti, self.scheme)].append((rec, ti))
        return idx

    def take(self, cand, r, pred=None):
        r.shuffle(cand)
        for rec, ti in cand:
            if rec["norm_sha256"] in self.claimed:
                continue
            if pred is not None and not pred(rec, ti):
                continue
            self.claimed.add(rec["norm_sha256"])
            return rec, ti
        return None


def add_examples(card, pool, idx, r):
    exs = []
    if not card["ex_on"]:
        card["examples"] = exs
        return
    codes = card["codes"]
    for i, c in enumerate(codes):
        if c["residual"]:
            continue
        for _ in range(r.choice([1, 2])):
            def only(rec, ti, i=i):
                if "\n" in rec["text"] or len(rec["text"]) > 220:
                    return False
                return [j for j, cc in enumerate(codes) if not cc["residual"] and cond(cc["condition"], rec, ti, card["scheme"])] == [i]
            got = pool.take(list(idx.get(i, [])), r, only)
            if got:
                rec, ti = got
                exs.append({"code": i, "text": rec["text"], "record_id": rec["record_id"], "norm": rec["norm_sha256"],
                            "ti": ti})
    card["examples"] = exs


def _bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def s7_groups(card, pool, idx, r, plan, stats):
    codes = card["codes"]
    n = len(codes)
    res_i = n - 1
    nonres = list(range(n - 1))
    made, gi, fails = 0, 0, 0
    abst = {}
    mix = [0, 0, r.random()]
    from samplers import YesCtl
    yctl = YesCtl(plan, card.get("card_id"))     # repair r1 (G7): per-card yes-rate controller on emitted rows
    while made < plan["n_rows"] and fails < 40:
        gi += 1
        r.random()
        # per-card choice-row controller (repair r1: name modes are shares of choice rows; twins included)
        if mix[1] < plan["choice_share"] * (mix[0] + 1) - mix[2]:
            if n >= 20:
                k = n if r.random() < 0.55 else r.randint(10, min(19, n - 1))
            else:
                k = r.randint(3, 4) if r.random() < 0.36 else r.randint(5, n) if n >= 5 else r.randint(3, n)
            others = [i for i in nonres]
            r.shuffle(others)
            slots = [res_i] + others[:k - 1]
            # stratified residual gold (repair r1, G10 abstain 1/k +/- 2 pp per bucket): the residual is gold when the
            # card's running residual-gold count is >= 0.5 below sum(1/k) over its emitted choice rows (twins included,
            # which never have a residual gold); otherwise a uniform non-residual shown code
            ab = abst.setdefault(_bucket(k), [r.random() - 0.5, 0])
            if (ab[0] + 1.14 / k) - ab[1] >= 0.5:     # 1.14: this anchor's expected defswap twin (never residual)
                gold = res_i
            else:
                gold = r.choice(slots[1:])
            got = pool.take(list(idx.get(gold, [])), r)
            if got is None and gold != res_i:
                # repair r1 (G10 abstain 1/k): a code whose records are used up hands the gold slot to another shown
                # non-residual code, so the residual keeps its 1/k gold share (it used to absorb these redraws)
                alts = [g for g in slots if g != res_i and g != gold]
                r.shuffle(alts)
                for g2 in alts:
                    got = pool.take(list(idx.get(g2, [])), r)
                    if got is not None:
                        gold = g2
                        stats["s7_gold_moved_to_other_code"] += 1
                        break
            if got is None:
                fails += 1
                stats["s7_no_unit"] += 1
                continue
            rec, ti = got
            # G10 gold letter (repair r1): stored option order is a seeded shuffle (it used to put the residual first)
            slots = list(slots)
            r.shuffle(slots)
            row = {"form": "choice", "rec": rec, "ti": ti, "options": slots, "gold": gold}
        else:
            r.random()
            want = yctl.want()
            cand = [u for code_i, us in idx.items() for u in us]
            got = None
            # the drawn yes/no answer is kept: asked codes are tried in random order until one has an unclaimed unit
            # with that answer (a re-draw of the answer would bias the yes rate toward the more common "no")
            for X in r.sample(nonres, len(nonres)):
                got = pool.take(list(cand), r, lambda rec, ti: cond(codes[X]["condition"], rec, ti, card["scheme"]) == want)
                if got is not None:
                    break
            yctl.result(got is not None)
            if got is None:
                fails += 1
                stats["s7_no_unit_yn"] += 1
                continue
            rec, ti = got
            row = {"form": "yn", "rec": rec, "ti": ti, "ask": X, "gold": int(want), "wkind": "fits"}
        fails = 0
        row["gid"] = gi
        group = [row]
        if r.random() < plan["twin_p"]:
            tw = s7_defswap(card, row, r)
            if tw is not None:
                group.append(tw)
                stats["twin_defswap"] += 1
        if row["form"] == "yn" and r.random() < plan["neg_p"] + plan["dneg_p"]:
            group.append({**row, "neg": 1, "neg_form": r.randrange(2), "gold": 1 - row["gold"], "rel": "complement",
                          "twin_kind": "neg", "twin_of": "anchor"})
            if r.random() < plan["dneg_p"] / (plan["neg_p"] + plan["dneg_p"]):
                group.append({**row, "neg": 2, "rel": "equiv", "twin_kind": "dneg", "twin_of": "anchor"})
        mix[0] += len(group)
        mix[1] += sum(1 for sp in group if sp.get("form") == "choice")
        # repair r1 (G10 abstain): with plan["_fb"] the emitting loop counts EMITTED choice rows (s7_note_choice);
        # counting at yield time also counted groups the renderer later dropped
        plan["_abst"], plan["_res_i"], plan["_abst_r"] = abst, res_i, r
        if not plan.get("_fb"):
            for sp in group:
                if sp.get("form") == "choice":
                    s7_note_choice(plan, sp)
        made += len(group)
        yield group


def s7_note_choice(plan, sp):
    a = plan["_abst"].setdefault(_bucket(len(sp["options"])), [plan["_abst_r"].random() - 0.5, 0])
    a[0] += 1 / len(sp["options"])
    a[1] += int(sp["gold"] == plan["_res_i"])


def swapped_codes(codes, X, Y):
    out = [dict(c) for c in codes]
    out[X] = dict(codes[X], condition=codes[Y]["condition"])
    out[Y] = dict(codes[Y], condition=codes[X]["condition"])
    return out


def s7_answer(codes, row, scheme):
    if row["form"] == "choice":
        g = first_fit(codes, row["rec"], row["ti"], scheme)
        return g if g in row["options"] else None
    return int(cond(codes[row["ask"]]["condition"], row["rec"], row["ti"], scheme))


def s7_defswap(card, row, r):
    """MR15 emitted twin: two non-residual codes trade definitions; gold follows the definition (asserted only
    when the record fits at most one non-residual code; otherwise solver A's recompute)."""
    codes = card["codes"]
    X = row["gold"] if row["form"] == "choice" else row["ask"]
    if codes[X]["residual"]:
        return None
    g0 = s7_answer(codes, row, card["scheme"])
    cands = [Y for Y in range(len(codes) - 1) if Y != X and (row["form"] == "yn" or Y in row["options"])]
    r.shuffle(cands)
    for Y in cands:
        sw = swapped_codes(codes, X, Y)
        g = s7_answer(sw, row, card["scheme"])
        if g is not None and g != g0:
            return {**row, "swap": [X, Y], "gold": g, "twin_kind": "defswap", "twin_of": "anchor"}
    return None


# ------------------------------------------------------------------------------------------------ rows
def question(card, row, rid):
    from rows import yn_question
    sch = card["scheme"]
    if row["form"] == "choice":
        q = L.Q_CHOICE["s7"][int(uhash(rid, "q") * len(L.Q_CHOICE["s7"]))]
    else:
        q = yn_question("fits", int(uhash(card["card_id"], rid, "q") * 97), card["qnames"][row["ask"]], "text",
                        row.get("neg", 0), row.get("neg_form", 0))
    if sch == "mams_atsa":
        terms = row["rec"]["ann"]["terms"]
        T = terms[row["ti"]]["term"]
        Ls = ", ".join(t["term"] for t in terms)
        fr = L.ATSA_FRAME[int(uhash(rid, "atsa") * 2)]
        q = fr.format(T=T, L=Ls) + " " + q
    return q


def render_row(card, row, rid, st, wording, short):
    from fmt1 import card as fcard
    c = card
    if row.get("swap"):
        c = dict(card, codes=swapped_codes(card["codes"], *row["swap"]))
    ir = card_ir(c)
    q = question(card, row, rid)
    if short:
        text = "Definitions for this task\n" + fcard.render_card(ir, st)
        fields = {"card": None, "instructions": fcard.render_instructions(st, question=q, wording=wording, card_text=text)}
        layout = "L8"
    elif row["form"] == "yn":
        fields = {"card": fcard.render_card(ir, st), "instructions": fcard.render_instructions(st, question=q, wording=wording)}
        layout = "L1"
    else:
        fields = {"card": None, "instructions": fcard.render_instructions(st, question=q, wording=wording,
                                                                          card_text=fcard.render_card(ir, st))}
        layout = "L6"
    fields["state"] = row["rec"]["text"]
    if row["form"] == "choice":
        opts = [card["qnames"][i] for i in row["options"]]
        gold = card["qnames"][row["gold"]]
        qtype = "choice"
    else:
        opts, gold, qtype = None, row["gold"], "noul"
    out = {"id": rid, "qtype": qtype, "options": opts, "gold": gold, **fields}
    return out, ir, q, layout
