"""F12 round-1 builder: card plan, row emission (fmt1 render + loader_check + real-tokenizer length), twins,
relations and sidecar.

  f12build.py <mode> [--shard i/n]     mode: cand (1.5 x 2,700 training rows), qc (>= 5,000 QC rows), dev (400 S5)
Outputs: out/parts/<mode>_<shard>.jsonl (+ .side.jsonl, .rel.jsonl); f12qc.py merge joins them.
"""
from __future__ import annotations

import collections
import copy
import datetime
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "formats" / "formats-1"))
import f12cards as C  # noqa: E402
import f12forms as F  # noqa: E402
import f12lex as L  # noqa: E402
import f12render as RD  # noqa: E402
import f12samp as SM  # noqa: E402
import f12solve_a as A  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
from fmt1 import labels as flabels  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402

FAM, SPEC_ID = "F12", "F12.G0.v7"
GEN_VERSION = "F12-gen r1.0 (py3.12, sqlite3, jsonschema 4.26.0, PyYAML 6.0.3)"
OUT = HERE.parent / "out"
PARTS = OUT / "parts"
SEED = 20261003
LICENCE = "CC0 1.0 (program-generated)"
ADMIT = {"memo", "email_thread", "json", "yaml", "markdown_table", "html_snippet", "bullet_sop"}
MODES = {"cand": 1.5, "qc": None, "dev": None}
QC_ROWS = 5200
TOKEN_CAP = 7900
YN_FORMS = {"Y-CALLX", "Y-ASK", "Y-FIT", "Y-DIRECT", "Y-VALID", "Y-CORRECT"}
P_NEG = 0.125  # share of yes/no base rows that carry a T-NEG unit (>= 10% negated, >= 2% double-negated)


def log(msg):
    with open(HERE.parent / "tmp" / "build.log", "a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


# ------------------------------------------------------------------------------------------------ packs and plan
_PACKS = None


def packs():
    global _PACKS
    if _PACKS is None:
        ps, _ = L.all_packs()
        _PACKS = ps
    return _PACKS


def plan_cards():
    """Training cards (55, one pack each) and S5 cards (6 held-out packs). Deterministic."""
    ps = packs()
    rng = random.Random(SEED)
    order = list(range(len(ps)))
    rng.shuffle(order)
    s5_idx = order[:6]
    tr_idx = order[6:6 + sum(C.PLAN_R1.values())]
    cards = []
    keys = set()
    i = 0
    for smp, n in C.PLAN_R1.items():
        for j in range(n):
            pk = ps[tr_idx[i]]
            i += 1
            cards.append(_card(pk, smp, f"F12-{smp}-c{j + 1:02d}", rng, keys, j, n))
    # antithetic card yes rates (repair r1, G10 aggregate 50 +/- 2 per cell): within a sampler, card 2i+1 takes
    # 1 - the rate of card 2i, so every rate stays uniform 20-80% and the aggregate sits at 50%
    by = collections.defaultdict(list)
    for c in cards:
        by[c["sampler"]].append(c)
    for cs in by.values():
        for a, b in zip(cs[0::2], cs[1::2]):
            b["yes_rate"] = round(1 - a["yes_rate"], 3)
    # repair r2 (G6 yes/no view c 0.539 vs 0.502; G7 raw yes/no words shared by 3 cards at 71% yes): which card
    # gets which rate is now chosen so that card-text features shared by several cards carry no yes-rate signal
    # (same multiset of rates, same within-sampler antithetic pairs; only the pairing/assignment changes)
    assign_yes_rates(cards)
    s5 = []
    for j, ix in enumerate(s5_idx):
        s5.append(_card(ps[ix], "S5", f"F12-S5-c{j + 1:02d}", rng, keys, j, len(s5_idx)))
    return cards, s5


_CF_TOK = re.compile(r"(?u)\b\w\w+\b")


def card_feats(card):
    """Words / word pairs of the card text (the yes/no `card` field: card sentences, examples, few-shot block; G6
    view c) plus the definition style (layout)."""
    parts = [s for _, s in card["sems"]]
    for blk in (card.get("_examples"), card.get("_fewshot")):
        if blk:
            parts.append(json.dumps(blk, sort_keys=True, ensure_ascii=False))
    f = set()
    for p in parts:
        w = _CF_TOK.findall(p.lower())
        f.update(w)
        f.update(a + " " + b for a, b in zip(w, w[1:]))
    f.add("#style=" + card["defs_style"])
    # repair r3 (G7 raw yes/no words over 2 cards, e.g. a limit value shared by two packs): the card's catalog
    # (tool params, limits, units, choices, scopes) is on every row of the card too; tagged so the card text keeps
    # its own weight
    for t in card.get("_tools") or []:
        txt = json.dumps({k: t.get(k) for k in ("params", "pre", "scope", "returns", "roles", "oword")}, sort_keys=True,
                         ensure_ascii=False, default=str)
        w = _CF_TOK.findall(txt.lower())
        f.update("@" + x for x in w)
    return f


RATE_SEED = 77  # local-search seed of assign_yes_rates (fixed; see tmp/t_g6emu.py)


def assign_yes_rates(cards, iters=40000, seed=None):
    """Keep the drawn rates as within-sampler antithetic pairs (+d / -d around 0.5; odd sampler: one card keeps its
    own rate) but choose the pairing, the pair values and the signs so that every set of cards sharing a visible
    feature has rate deviations summing to about 0 (min sum_f w_f D_f^2 / |S_f|). Deterministic local search."""
    rng = random.Random(SEED + (RATE_SEED if seed is None else seed))
    n = len(cards)
    sets = collections.defaultdict(list)
    for i, c in enumerate(cards):
        for t in card_feats(c):
            sets[t].append(i)
    uniq = collections.Counter(tuple(v) for v in sets.values() if 2 <= len(v) <= n - 1)
    F = list(uniq)
    W = [uniq[s] ** 0.5 / len(s) for s in F]
    cf = [[] for _ in range(n)]
    for j, s in enumerate(F):
        for i in s:
            cf[i].append(j)
    # repair r4 (G10 qc Y-CORRECT yes 61%: the form sits on a few S3 cards, so its aggregate followed those cards'
    # rates): every yes/no form's expected aggregate deviation sum_c w_cF r_c (w = the card's expected share of the
    # form's rows: rows per card x yes/no share / number of yes/no forms on the card) is kept at about 0 too
    fw = form_weights(cards)
    FN = sorted(fw)
    cw = [[] for _ in range(n)]
    for j2, fm in enumerate(FN):
        for i, x in fw[fm].items():
            cw[i].append((j2, x))
    by = collections.defaultdict(list)
    for i, c in enumerate(cards):
        by[c["sampler"]].append(i)
    pairs, devs, single = [], [], {}
    for smp, ix in by.items():
        for a, b in zip(ix[0::2], ix[1::2]):
            pairs.append([a, b])
            devs.append(cards[a]["yes_rate"] - 0.5)
        if len(ix) % 2:
            single[smp] = ix[-1]
    sval = {i: cards[i]["yes_rate"] - 0.5 for i in single.values()}
    r = [0.0] * n

    def rates():
        out = [0.0] * n
        for (a, b), d in zip(pairs, devs):
            out[a], out[b] = d, -d
        for i, v in sval.items():
            out[i] = v
        return out

    r = rates()
    D = [0.0] * len(F)
    D2 = [0.0] * len(FN)
    for i in range(n):
        for j in cf[i]:
            D[j] += r[i]
        for j2, x in cw[i]:
            D2[j2] += x * r[i]

    def delta(ch):  # ch: {card: new_dev}; returns objective change, applies nothing
        acc = collections.defaultdict(float)
        acc2 = collections.defaultdict(float)
        for i, v in ch.items():
            dv = v - r[i]
            for j in cf[i]:
                acc[j] += dv
            for j2, x in cw[i]:
                acc2[j2] += x * dv
        dl = sum(W[j] * ((D[j] + x) ** 2 - D[j] ** 2) for j, x in acc.items())
        dl += FORM_LAMBDA * sum((D2[j] + x) ** 2 - D2[j] ** 2 for j, x in acc2.items())
        return dl, (acc, acc2)

    obj = sum(w * d * d for w, d in zip(W, D)) + FORM_LAMBDA * sum(d * d for d in D2)
    T0 = obj / max(1, len(F)) * 4 + 1e-9
    smp_pairs = collections.defaultdict(list)
    for p, (a, b) in enumerate(pairs):
        smp_pairs[cards[a]["sampler"]].append(p)
    smps = sorted(smp_pairs)
    for it in range(iters):
        T = T0 * (1 - it / iters) + 1e-12
        m = rng.random()
        if m < 0.3:  # flip a pair's sign
            p = rng.randrange(len(pairs)); a, b = pairs[p]
            ch = {a: r[b], b: r[a]}
            move = ("flip", p)
        elif m < 0.6:  # swap values of two pairs
            p, q = rng.sample(range(len(pairs)), 2)
            (a, b), (c, d) = pairs[p], pairs[q]
            ch = {a: r[c], b: r[d], c: r[a], d: r[b]}
            move = ("val", p, q)
        else:  # re-pair inside a sampler (or swap the odd card in)
            smp = rng.choice(smps)
            ps = smp_pairs[smp]
            if smp in single and rng.random() < 0.25:
                p = rng.choice(ps); k = rng.randrange(2); a = pairs[p][k]; s = single[smp]
                ch = {s: r[a], a: r[s]}
                move = ("single", smp, p, k)
            elif len(ps) >= 2:
                p, q = rng.sample(ps, 2)
                (a, b), (c, d) = pairs[p], pairs[q]
                ch = {b: r[d], d: r[b]}  # (a,b),(c,d) -> (a,d),(c,b) keeping each pair's values on a / c
                move = ("pair", p, q)
            else:
                continue
        dl, (acc, acc2) = delta(ch)
        if dl < 0 or rng.random() < pow(2.718281828, -dl / T):
            for i, v in ch.items():
                r[i] = v
            for j, x in acc.items():
                D[j] += x
            for j, x in acc2.items():
                D2[j] += x
            obj += dl
            if move[0] == "pair":
                p, q = move[1], move[2]
                pairs[p][1], pairs[q][1] = pairs[q][1], pairs[p][1]
            elif move[0] == "single":
                _, smp, p, k = move
                s = single[smp]; a = pairs[p][k]
                pairs[p][k] = s; single[smp] = a
                sval = {single[x]: r[single[x]] for x in single}
    for i, c in enumerate(cards):
        c["yes_rate"] = round(0.5 + r[i], 3)
    worst = max((abs(d) / len(s) ** 0.5 for d, s in zip(D, F)), default=0.0)
    return {"features": len(F), "obj": round(obj, 4), "max_dev_over_sqrt_n": round(worst, 4),
            "form_dev": {fm: round(d, 4) for fm, d in zip(FN, D2)}}


FORM_LAMBDA = 200.0  # repair r4: weight of the per-form aggregate terms in assign_yes_rates


def form_weights(cards):
    """{yes/no form: {card index: expected share of the form's rows}} from the plan (rows per card x yes/no share /
    number of the card's yes/no forms)."""
    ncard = collections.Counter(c["sampler"] for c in cards)
    raw = collections.defaultdict(dict)
    for i, c in enumerate(cards):
        yn = [f for f in c["forms"] if f in YN_FORMS]
        rows = C.ROWS_R1.get(c["sampler"], 0) / max(1, ncard[c["sampler"]]) * (
            1 - P_CHOICE.get(c["sampler"], P_CHOICE_DEFAULT))
        for f in yn:
            raw[f][i] = rows / len(yn)
    return {f: {i: x / sum(d.values()) for i, x in d.items()} for f, d in raw.items()}


SCHEME_OFFSET = 0.21  # repair r3: shifts which cards get masked / swapped (tmp/t_scheme.py grid on realised counts)
# repair r6: was 0.96 / (0.32, 0.55): build 16 swapped 6.29% cand / 6.24% qc (G10 4-6%); one card holds ~1-3% of the
# choice rows, so no band on the old offset passes; tmp/t_scheme4.py picks the setting that passes most often when
# the per-card C-OUT / C-ACT counts move by 20% (0.78 of draws; build-16 counts: masked 12.5 / 10.9%, swapped 4.3 / 4.4%)
SCHEME_BANDS = (0.27, 0.41)  # masked x < a, swapped a <= x < b (repair r2: was 0.34 / 0.52, which gave swapped
# C-OUT / C-ACT rows 3.3% of choice rows, G10 needs 4-6%; masked stays 10-15%)


def _card(pk, smp, cid, rng, keys, j, n):
    for attempt in range(200):
        pol = {"invalid": rng.choice("AB") if smp != "S3" else "A", "chain": False, "tie": False, "fresh": None,
               "role": False}
        chain_ok = any(a in L.OTHER_ID_ACTIONS for a in pk["actions"][:13])
        if smp == "S6":
            pol["role"] = j < round(0.7 * n) + 1
            pol["tie"] = j % 2 == 0
            pol["chain"] = chain_ok and j < 4
        if smp == "S2":
            pol["chain"] = chain_ok and j < 2
        if smp in ("S2", "S6"):
            pol["role"] = pol["role"] or (smp == "S2" and rng.random() < 0.3)
            pol["tie"] = pol["tie"] or (smp == "S2" and rng.random() < 0.3)
        if smp == "S1":
            pol["tie"] = rng.random() < 0.3
        if smp in ("S2", "S4", "S6"):
            pol["fresh"] = rng.choice([None, 30, 60, 120, 240])
        forms = list(C.FORMS[smp])
        keep_always = ("C-OUT", "C-TOOL") if smp != "S3" else ()
        drop = [f for f in forms if rng.random() < (0.15 if smp != "S3" else 0.35) and f not in keep_always]
        forms = [f for f in forms if f not in drop] or forms
        if (smp == "S2" and j >= n - 3) or (smp == "S6" and j >= n - 4):
            forms = forms + ["C-INV"]
        scheme = "plain"
        if any(f in forms for f in ("C-OUT", "C-ACT")):
            x = rng.random()
            # repair r1 (G10 swapped 4-6% / masked 10-15% of choice rows): a low-discrepancy sequence per sampler
            # instead of a free draw, so the realised card shares hit the targets (rng draw kept for the stream)
            x = (j * 0.6180339887 + 0.11 * (attempt % 3) + SCHEME_OFFSET) % 1.0
            scheme = "masked" if x < SCHEME_BANDS[0] else ("swapped" if x < SCHEME_BANDS[1] else "plain")
        syntax = rng.choice(["json", "func"]) if smp == "S3" else ("cli" if smp == "S5" else "none")
        key = (tuple(sorted(forms)), json.dumps(pol, sort_keys=True), scheme, syntax)
        if key not in keys:
            keys.add(key)
            break
    else:
        raise RuntimeError("card key collision")
    dstyle = rng.choice(["one_line", "one_line_examples", "decision_list", "one_line_examples"])
    tools = EXTRA_TOOLS[smp](pk) if smp in EXTRA_TOOLS else L.make_tools(pk, smp in ("S1", "S6"), pol["chain"])
    for t in tools:
        t["oword"] = pk["etypes"][t["o"]]["word"]
    card = {"id": cid, "sampler": smp, "pack": pk["id"], "pol": pol, "forms": forms, "names_scheme": scheme,
            "syntax": syntax, "defs_style": dstyle, "yes_rate": round(rng.uniform(0.2, 0.8), 3),
            "out_set": rng.randrange(len(RD.OUT_NAME_SETS)), "dimw": pk["dim"]["words"], "key": list(key),
            "persona_seed": pk["persona_seed"]}
    card["sems"] = C.sem_sentences(card, pk)
    card["_tools"] = tools
    card["_examples"] = None
    card["_fewshot"] = None
    if EXTRA_EXAMPLES and dstyle == "one_line_examples":
        card["_examples"] = EXTRA_EXAMPLES(card, pk, 1 + (j % 2))
    if EXTRA_EXAMPLES and smp in ("S1", "S2", "S4", "S6") and j == 5:
        card["_fewshot"] = EXTRA_EXAMPLES(card, pk, 2 + (j % 2), fewshot=True)
    return card


def card_names(card, pk):
    """Masked IDs (fmt1 MSxx) or swap words (fmt1 swap pool) for the four outcome kinds; plain -> None."""
    if card["names_scheme"] == "plain":
        return None
    if card["names_scheme"] == "masked":
        sch = ["MS01", "MS02", "MS03", "MS04"][int(hashlib.sha256(card["id"].encode()).hexdigest(), 16) % 4]
        ids = flabels.masked_ids(sch, 4, "f12-" + card["id"])
        return {"scheme": sch, "map": dict(zip(["CALL", "ASK", "UNABLE", "ANSWER"], ids))}
    bad = {"call", "ask", "answer", "unable", "cannot", "say", "act", "do", "tool"}
    lex = " ".join([e["word"] for e in pk["etypes"]] + list(pk["params"]) + pk["roles"] + pk["dim"]["values"]
                   + pk["status"] + [pk["dim"]["words"]]).lower()
    words = [w["word"] for w in fpool.swap_words() if w["word"].lower() not in bad
             and w["word"].lower() not in lex and not any(b in w["word"].lower() for b in bad)]
    r = random.Random("swap-" + card["id"])
    r.shuffle(words)
    ws = [w.capitalize() for w in words[:4]]
    return {"scheme": "swap", "map": dict(zip(["CALL", "ASK", "UNABLE", "ANSWER"], ws))}


def borrow_pool(card, cards):
    """Inert tools borrowed from other training packs (never S5 packs), R1-22."""
    out = []
    ps = {p["id"]: p for p in packs()}
    for c in cards:
        if c["pack"] == card["pack"] or c["sampler"] == "S5":
            continue
        q = ps[c["pack"]]
        for t in c["_tools"]:
            if t["vid"] == "base" and t["a"] != "look up" and len(t["params"]) <= 2 and not t["returns"]:
                b = copy.deepcopy(t)
                b.update(borrowed=True, src=q["id"], oword=q["etypes"][t["o"]]["word"], o=-1,
                         dimw=q["dim"]["words"])
                out.append(b)
    return out


# ------------------------------------------------------------------------------------------------ styles
_STY = {}


def styles_for(held_out):
    if held_out not in _STY:
        _STY[held_out] = [s for s in fpool.styles(held_out=held_out) if s["container"] in ADMIT]
    return _STY[held_out]


# ------------------------------------------------------------------------------------------------ tokens
_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from transformers import AutoTokenizer
        _TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    return _TOK


def served_tokens(row):
    dio = fcard._dio()
    with fcard._serving(dio, len(row.get("options") or [1, 2])):
        user = dio.user_msg(row, None)
        text = dio.render_chat(tokenizer(), dio.CYGNET_SYSTEM, user)
    return len(tokenizer()(text)["input_ids"])


# ------------------------------------------------------------------------------------------------ rendering
def sha(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()


def structure_hash(R, card):
    S = R["S"]
    canon = {"pack": card["pack"], "pol": S["pol"], "now": S["now"], "role": S["role"],
             "tools": [(t.get("src", card["pack"]), t["name"], t["vid"]) for t in S["tools"]],
             "records": S["records"], "conv": [{k: v for k, v in c.items() if not k.startswith("_")} for c in S["conv"]],
             "stored": S["stored"], "call": S.get("call"), "form": R["form"], "q": R.get("q"),
             "cases": R.get("cases_struct")}
    return sha(canon)


def prepare_texts(R, pk, rng):
    """Fix the surface choices that live in user text (cue templates, correction cue) once per unit."""
    for c in R["S"]["conv"]:
        if c["who"] == "user":
            for s in c["st"]:
                if s["t"] == "req" and "_text" not in s:
                    s["_text"] = RD.request_text(s, pk, rng)
                if s["t"] == "corr" and "_text" not in s:
                    s["_text"] = rng.choice(RD.CORR)
    for ref, st in R.get("cases") or []:
        for s in st:
            if s["t"] == "req" and "_text" not in s:
                s["_text"] = RD.request_text(s, pk, rng)


def _st_key(s):
    return json.dumps({k: v for k, v in s.items() if not k.startswith("_")}, sort_keys=True, default=str)


def share_texts(R, R2):
    """A twin keeps the base row's surface text for every statement it shares (only the decisive fact moves)."""
    tx = {}
    for c in R["S"]["conv"]:
        for s in c.get("st") or []:
            if "_text" in s:
                tx.setdefault(_st_key(s), s["_text"])
    for c in R2["S"]["conv"]:
        for s in c.get("st") or []:
            if "_text" not in s and _st_key(s) in tx:
                s["_text"] = tx[_st_key(s)]
            elif s["t"] == "req" and "_text" in s:
                pass


def depth_of(R):
    """Section 2 weight table on the decisive path (solver A's derivation)."""
    S, res = R["S"], R["res"]
    if res is None:
        return 1
    d = 1
    o = res.get("outcome")
    src = res.get("src", {})
    if o == "CALL" and res.get("tool"):
        T = next(t for t in S["tools"] if t["name"] == res["tool"])
        for p in T["params"]:
            if p["required"] and src.get(p["name"]) in ("record", "tool", "stored", "earlier", "continuation",
                                                       "reldate"):
                d += 1
        if T["pre"]:
            d += 1
        if res.get("tie"):
            d += 1
        if res.get("chain"):
            d += 1
    elif o in ("ASK", "UNABLE"):
        layers = set()
        for t in S["tools"]:
            ck = res["checks"][t["name"]]
            if t["a"] == res["a"] and t["o"] == res["o"]:
                if ck["fails"]:
                    layers.add(ck["fails"][0])
                elif ck["rejects"]:
                    layers.add("value")
        d += len(layers & {"precondition", "role", "value", "scope"})
        if res.get("unclear"):
            d += 1
    elif o == "ANSWER" and res.get("answer") in ("record", "stored"):
        d += 1
        if res.get("answer") == "stored" and S["pol"]["fresh"] is not None:
            d += 1
    if S["pol"]["role"] and o in ("CALL", "UNABLE"):
        d += 1
    return d


F.DEPTH_FN = depth_of  # repair r4 (f12forms.forward_matched)


def render_row(R, card, pk, style, wid, mode, rid, neg=0, card_mode="full"):
    names = card.get("_names")
    card_r = dict(card)
    card_r["names"] = names
    layout = "compact" if len(R["S"]["tools"]) >= 26 else "full"
    doc = RD.state_doc(R, pk, card_r, random.Random(rid), layout)
    wd = C_WORDINGS[wid]["text"]
    form = R["form"]
    if R["qtype"] == "noul":
        q = RD.YN[(form, R["framing"])][neg].format(T=R["q"].get("tool", ""))
    else:
        q = RD.QUESTIONS[form].format(p=R["q"].get("param", ""), T=R["q"].get("tool", ""))
    ir = None if card_mode == "none" else C.card_ir(card, pk, card_mode, examples=card.get("_examples"))
    if form == "C-INV":
        ir = copy.deepcopy(ir)
        ir["blocks"].append({"type": "para", "text": fcard.inverted_frame(R["frame"]) + " Judge each request only "
                             "by what it states."})
    if R["qtype"] == "choice":
        texts = [RD.opt_text(o, R, card_r) for o in R["opts"]]
        defs = RD.option_defs(R, card_r, texts)
        if defs:
            ir = copy.deepcopy(ir) if ir else {"title": None, "blocks": []}
            ir["blocks"].append({"type": "defs", "variant": "DV01", "heading": None, "entries": defs})
            if names:
                ir["blocks"].append({"type": "para", "text": "Each option means exactly the definition written "
                                     "next to it, even if its name is a familiar word that usually means something "
                                     "else. This applies to the option names only; every other word keeps its usual "
                                     "meaning."})
        gold = texts[R["opts"].index(R["gold"])]
        f, res = fcard.render_and_check(style, doc=doc, question=q, qtype="choice", gold=gold, card=ir,
                                        options=texts, wording=wd, row_id=rid, seed="f12-" + rid)
        return f, texts, gold, q, ir, fcard.must_show(ir, question=q, wording=wd)
    gold = R["gold"] if neg != 1 else 1 - R["gold"]
    f, res = fcard.render_and_check(style, doc=doc, question=q, qtype="noul", gold=gold, card=ir, wording=wd,
                                    row_id=rid, seed="f12-" + rid)
    return f, None, gold, q, ir, fcard.must_show(ir, question=q, wording=wd)


C_WORDINGS = C.wordings()


def wording_for(card, form, rng):
    ws = [w for w, r in C_WORDINGS.items() if form in r["forms"] or "any" in r["forms"]]
    pool = card.setdefault("_wpool", {})
    if form not in pool:
        r = random.Random("w-" + card["id"] + form)
        own = [w for w, rr in C_WORDINGS.items() if form in rr["forms"]]
        gen = [w for w, rr in C_WORDINGS.items() if "any" in rr["forms"]]
        r.shuffle(own)
        r.shuffle(gen)
        pool[form] = own[:3] + gen[:2]
    return rng.choice(pool[form] or ws)


def card_free_ok(R, pk=None):
    S, res = R["S"], R["res"]
    if R["form"] in ("C-VALUE", "C-DEFECT", "Y-VALID", "Y-CORRECT", "C-INV") or res is None:
        return False
    o = res["outcome"]
    if R["form"] == "Y-DIRECT" and o == "UNABLE":
        return False
    if S["stored"] or len(S["conv"]) > 1 or any(t["returns"] for t in S["tools"]):
        return False
    req, _ = A.request_of(S)
    if req["cue"] == "catalog":
        return False
    if S["records"] and not (o == "ANSWER" and _cf_answer_record(S, req)):
        return False
    if any(s["t"] in ("qual", "corr") or (s["t"] == "val" and (s.get("alts") or s["p"] is None
                                                               or A.REL.match(s["v"] or "")))
           for s in S["conv"][-1]["st"]):
        return False
    if (S["pol"]["role"] or S["pol"]["tie"]) and pk is None:
        return False
    if pk is not None and not _pol_free(R, pk):
        # repair r3 (G11): role / tie cards may be card-free on rows where no card policy is decisive (G0 8); the
        # same test as G3: the label holds with POL-INVALID A and B and with no role / tie rule
        return False
    if o == "UNABLE":
        return all(t["a"] != req["a"] or t["o"] != req["o"] for t in S["tools"])
    if o == "ASK":
        T = [t for t in S["tools"] if res["checks"][t["name"]]["fit"]]
        if len(T) != 1:
            return False
        ck = res["checks"][T[0]["name"]]
        if ck["rejects"] or ck["unclear"] or len(ck["missing"]) != 1:
            return False
        p = next(p for p in T[0]["params"] if p["name"] == ck["missing"][0])
        return p["type"] != "boolean" and all(t["pre"] is None and t["scope"] is None for t in S["tools"]
                                              if not t.get("borrowed"))
    if o == "CALL":
        T = next(t for t in S["tools"] if t["name"] == res["tool"])
        if T["pre"] or T["scope"] or any(t["pre"] or t["scope"] for t in S["tools"] if not t.get("borrowed")):
            return False
        stated = {x["p"]: x["v"] for x in S["conv"][-1]["st"] if x["t"] == "val" and x["p"]}
        for p in T["params"]:
            if p["name"] not in res["vals"] or p["type"] in ("id", "enum", "string"):
                continue
            v = stated.get(p["name"])
            if v is None or not all(_cf_literal_ok(q, v, S["now"]) for t in S["tools"] for q in t["params"]
                                    if q["name"] == p["name"]):
                return False
        return True
    if o == "ANSWER":
        # R1-20: an info question no listed tool could serve (no listed tool has the read action on its object),
        # answered in the current request or in the only record shown (exact ID the user gives)
        if req["kind"] != "info" or any(t["a"] == req["a"] and t["o"] == req["o"] for t in S["tools"]):
            return False
        if S["records"]:
            return True  # _cf_answer_record held above
        return any(x["t"] == "val" and x["p"] == req.get("field") and x["v"] and not x.get("alts")
                   for x in S["conv"][-1]["st"])
    return False


def _pol_free(R, pk):
    S, res = R["S"], R["res"]
    for inv in ("A", "B"):
        try:
            r2 = A.solve(dict(S, pol=dict(S["pol"], invalid=inv, role=False, tie=False)), pk)
        except (AssertionError, ValueError):  # e.g. a tie that only POL-TIE breaks: the tie rule is decisive
            return False
        if (r2["outcome"], r2.get("tool")) != (res["outcome"], res.get("tool")):
            return False
    return True


def _cf_answer_record(S, req):
    """The one answer-bearing record of a card-free ANSWER row: the only record, carrying the exact ID the user gives
    and the asked field with a usable value."""
    if len(S["records"]) != 1 or not req.get("ref") or req["ref"][0] != "id" or not req.get("field"):
        return False
    f = dict((k, v) for k, v in S["records"][0]["fields"])
    return req["ref"][1] in f.values() and req["field"] in f and f[req["field"]] not in A.MARK_UNKNOWN


def _cf_literal_ok(p, text, now):
    """A CALL value on a card-free row (G0 8): stated literally in a form the tool takes, never a boundary value
    (at least one accepted step inside every limit), a relative date, a unit change or a rounding."""
    t = p["type"]
    if t in ("id", "enum", "string"):
        return True
    if t in ("integer", "decimal"):
        ok, v = A.accept(p, text, now)
        if not ok:
            return False
        step = A.Decimal(1) if t == "integer" else A.Decimal(1).scaleb(-p["places"])
        v = A.Decimal(str(v))
        return all(abs(v - A.Decimal(str(lim[0]))) > step for lim in (p.get("min"), p.get("max")) if lim)
    if t == "date":
        if A.REL.match(text.strip().lower()) or not A.accept(p, text, now)[0]:
            return False
        try:
            d = datetime.date.fromisoformat(text.strip())
        except ValueError:
            return False
        return all(abs((d - datetime.date.fromisoformat(lim[0])).days) > 1 for lim in (p.get("min"), p.get("max"))
                   if lim)
    return False


# ------------------------------------------------------------------------------------------------ main loop
# Per-sampler choice-form shares, set so the family mix meets section 8 (of F12 choice rows: C-OUT 20, C-ACT 17,
# C-TOOL 25, C-PARAM 8, C-DEFECT 15, C-VALUE 5, C-INV 10 %). C-DEFECT is S3's only choice form; C-VALUE is S4-only;
# inverted cards (C-INV) keep about three quarters of their choice rows on C-INV.
# C-TOOL rows of 20-60 options come only from S1 / S6 (S2 caps C-TOOL at 9 options), so S1 / S6 carry most C-TOOL
# rows and the option-count buckets (35 / 35 / 15 / 15 %) hold for the family.
CHOICE_SHARE = {"S1": {"C-OUT": 15, "C-ACT": 15, "C-TOOL": 60, "C-PARAM": 10},
                "S2": {"C-OUT": 30, "C-ACT": 27, "C-TOOL": 25, "C-PARAM": 18},
                "S4": {"C-OUT": 29, "C-ACT": 27, "C-PARAM": 16, "C-VALUE": 28},
                "S6": {"C-TOOL": 60, "C-OUT": 20, "C-ACT": 20},
                "S5": {"C-OUT": 24, "C-ACT": 22, "C-TOOL": 40, "C-PARAM": 14}}
INV_SHARE = 74
# target share of choice rows among the rows a card makes (twin and T-NEG rows included): yes/no share of F12 rows
# 45-55%; S3's only choice form is C-DEFECT, 15% of F12 choice rows
P_CHOICE = {"S3": 0.60}
P_CHOICE_DEFAULT = 0.52


# Card-free intent (section 8: a short or no card on about 15% of rows, only where card_free_ok holds): on these
# outcome-form attempts the sampler shows no record, stored result, look-alike, qualifier, unnamed value or catalog
# cue and lists no precondition / scope / returns tool. The intent is drawn before the outcome, so context presence
# stays flat across gold labels; S2 / S4 keep their stored-result and turn shapes (S4 none, S2 a small share).
P_CF = {"S1": 0.90, "S2": 0.40, "S6": 0.50}
# repair r1 (G11 short / no card): C-TOOL and C-ACT are outcome forms (G0 8 card_free_ok), so they may be card-free too
CF_FORMS = ("C-OUT", "C-PARAM", "Y-CALLX", "Y-ASK", "Y-FIT", "Y-DIRECT", "C-TOOL", "C-ACT")
P_SHORT = 0.95
NAMED_FORMS = ("C-OUT", "C-ACT")  # the only forms whose options show masked / swapped outcome names
CF_STATS = collections.Counter()  # diagnostics only
CF_WANT = {"cf": True, "no_records": True, "no_stored": True, "no_read": True, "p_look": 0.0, "p_name": 0.0, "p_unnamed": 0.0,
           "cue_ok": False, "catalog_ok": False, "no_chain": True}


# Short-card label parity (repair r3): card-free acceptance differs by label (G0 8 keeps T-KIND sets and some
# outcomes off card-free rows), so a cf-ok unit takes a short / no card only while none of its labels is
# over-represented among the (sampler, form)'s short rows: label short share <= the form's short share + SHORT_SLACK.
SHORT_N = collections.Counter()
SHORT_S = collections.Counter()
SHORT_SLACK = 0.12


def _short_label(outcome, qtype, gold):
    # yes/no rows: the label is the gold answer; choice rows: the outcome (which option kind is gold)
    return ("yn", gold) if qtype == "noul" else (outcome, "")


def short_ok(card, form, unit):
    k = (card["sampler"], form)
    tn = sum(v for (kk, _), v in SHORT_N.items() if kk == k)
    ts = sum(v for (kk, _), v in SHORT_S.items() if kk == k)
    sbar = ts / tn if tn else 0.0
    for RR, neg, _, _ in unit:
        res = RR.get("res") or {}
        g = (RR["gold"] if neg != 1 else 1 - RR["gold"]) if RR.get("qtype") == "noul" else ""
        L = (k, _short_label(res.get("outcome"), RR.get("qtype"), g))
        if SHORT_N[L] >= 4 and (SHORT_S[L] + 1) / (SHORT_N[L] + 1) > sbar + SHORT_SLACK:
            return False
    return True


def short_update(card, form, side, row):
    L = ((card["sampler"], form), _short_label(side.get("outcome"), row["qtype"], row["gold"]))
    SHORT_N[L] += 1
    SHORT_S[L] += side.get("card_mode") in ("short", "none")


def cf_want(card, form, rng):
    if form not in CF_FORMS or (card["_names"] and form in NAMED_FORMS):
        return {}
    pc = P_CF.get(card["sampler"], 0.0)
    if rng.random() < pc:
        return dict(CF_WANT)
    # stored results stay on 40-60% of S2 / S6 rows at a flat rate (section 4): card-free attempts show none, so the
    # other attempts of the same (card, form) show one more often (repair r3)
    return {"p_stored": min(0.95, 0.6 / (1 - pc))} if card["sampler"] in ("S2", "S6") and pc > 0 else {}


class FormPicker:
    """Yes/no vs choice: choice while the card's choice rows are below P_CHOICE of its rows; the choice form is the one furthest below its share of the card's choice rows
    made so far (failed builds do not count, so forms that reject often are retried). A form that keeps failing on a
    card (>= 12 fails per row made) is dropped for that card."""

    def __init__(self, card, rng):
        forms = card["forms"]
        self.rng = rng
        self.p_choice = P_CHOICE.get(card["sampler"], P_CHOICE_DEFAULT)
        self.yn = [f for f in forms if f in YN_FORMS]
        self.ch = [f for f in forms if f not in YN_FORMS]
        base = CHOICE_SHARE.get(card["sampler"], {})
        sh = {f: base.get(f, 10) for f in self.ch if f != "C-INV"}
        if "C-INV" in self.ch:
            tot = sum(sh.values()) or 1
            sh = {f: v * (100 - INV_SHARE) / tot for f, v in sh.items()}
            sh["C-INV"] = INV_SHARE
        tot = sum(sh.values()) or 1
        self.share = {f: v / tot for f, v in sh.items()}
        self.made = collections.Counter()
        self.fail = collections.Counter()

    def next(self):
        live = [f for f in self.ch if self.fail[f] < 12 * (self.made[f] + 1)]
        n_all = sum(self.made.values())
        n_ch = sum(self.made[f] for f in self.ch)
        if live and (not self.yn or n_ch < self.p_choice * (n_all + 1)):
            n = sum(self.made[f] for f in self.ch) + 1
            best = max(self.share[f] * n - self.made[f] for f in live)
            return self.rng.choice([f for f in live if self.share[f] * n - self.made[f] >= best - 1e-9])
        return self.rng.choice(self.yn) if self.yn else None


def _bal_key(ctx, R):
    """(key, weights, category) of a choice row spec for the C-OUT / C-ACT balance controller, else None."""
    g = R["gold"]
    if R["form"] == "C-OUT":
        return ("out",), {o: 0.25 for o in F.OUTS}, g[1]
    if R["form"] == "C-ACT":
        k = len(R["opts"])
        nc = sum(1 for o in R["opts"] if o[0] == "call")
        na = sum(1 for o in R["opts"] if o[0] == "ask")
        return ("act", F.bkt(k)), F.act_weights(nc, na, k), g[0]
    return None


def twin_over(ctx, R, R2):
    a, b = _bal_key(ctx, R), _bal_key(ctx, R2) if R2.get("form") else None
    if a is None or b is None:
        return False
    # repair r9 (G10 cand build 20: C-ACT "Say it cannot be done" gold 51 / 348 vs 1/k 34.5, binom p 0.005): twins
    # supply UNABLE / ANSWER on top of the soft base draw, which cannot go below zero, so each card bucket ended up to a
    # quarter row over; a C-ACT label-flip twin now needs its kind to stay at or under its expected count
    return F.bal(ctx).over(b[0], b[1], b[2], extra=(a[1], a[2]), tol=0.0 if R["form"] == "C-ACT" else 0.25)


def bal_update(ctx, card, side, row):
    b = F.bal(ctx)
    form = side["form"]
    g = side["gold_canon"]
    oc = [tuple(o) for o in side["opts_canon"]] if side.get("opts_canon") else None
    if form in YN_FORMS:
        na = b.n.setdefault(("yn_all",), {})  # repair r4: realised card yes share (Bal.yes bounds)
        na[int(row["gold"])] = na.get(int(row["gold"]), 0) + 1
        if not side.get("neg"):
            t = card["yes_rate"]
            b.add(("yn", form, side.get("framing")), {1: t, 0: 1 - t}, int(g))
            b.add(("yn_card",), {1: t, 0: 1 - t}, int(g))  # repair r4: card-level deficit
        return
    if not oc:
        return
    k = len(oc)
    if form in F.BUCKETS:
        b.add(("bk", form), F.bk_weights(ctx, form), F.bkt(k))
    if form == "C-OUT":
        b.add(("out",), {o: 0.25 for o in F.OUTS}, g[1])
    elif form == "C-ACT":
        nc = sum(1 for o in oc if o[0] == "call")
        na = sum(1 for o in oc if o[0] == "ask")
        b.add(("act", F.bkt(k)), F.act_weights(nc, na, k), g[0])
        if not side.get("twin_kind"):
            F.act_pend_clear(ctx, k)  # repair r7: the card's pending C-ACT class is made
        F.ACT_DEPTH[(card["sampler"], g[0] == "answer", row["meta"]["depth"])] += 1  # repair r4
    elif form == "C-DEFECT":
        b.add(("cdv", F.bkt(k)), {"valid": 1 / k, "defect": 1 - 1 / k}, "valid" if g[0] == "valid" else "defect")
        if CDEF_RECORD:
            CDEF_RECORD(ctx, oc, g)  # repair r4: defect class exposure
    elif form == "C-VALUE" and ("novalue",) in oc:
        b.add(("nv", F.bkt(k)), {"nv": 1 / k, "v": 1 - 1 / k}, "nv" if g[0] == "novalue" else "v")
    elif form == "C-PARAM" and ("nothing",) in oc:  # repair r9: Nothing gold by the card controller (f12forms.c_param)
        b.add(("np", F.bkt(k)), {"np": 1 / k, "p": 1 - 1 / k}, "np" if g[0] == "nothing" else "p")
    elif form == "C-TOOL" and ("none",) in oc:  # repair r9: None gold by the card controller (f12forms.c_tool)
        b.add(("nn", F.bkt(k)), {"nn": 1 / k, "c": 1 - 1 / k}, "nn" if g[0] == "none" else "c")
    F.mm_update(form, g, side["S"], row["meta"]["depth"])  # repair r7: structure cells by gold class (mm_forward)
    if form in ("C-TOOL", "C-ACT"):
        F.texp_add(ctx, oc, g)  # repair r4: per-card tool exposure
        F.depth_update(form, g, row["meta"]["depth"])  # repair r4: depth mix by gold class


# repair r8 (G6 choice d_metadata LR on build 18; ablation tmp/t_dabl.log: dropping the "first / last option in the
# text" kinds cut the C-VALUE excess 17.8 -> 6.8 and C-PARAM 13.8 -> 3.8; qc C-VALUE gold last 34 / 52 of the rows with
# two value options in the text, C-PARAM gold first 43 / 174 vs 31.8): the gold's rank among the options written in
# the rendered state is balanced on this worker. RK[form] = [first, last] excess of "pick the option written first /
# last" over 1 / k, summed over the emitted rows (all rows of the form, twins and abstain golds included). On a
# single-row unit whose gold is written in the state, the shown distractors may be swapped for unshown ones of the
# same class (C-VALUE: written values of the same source class; C-PARAM: same named-in-the-conversation class, so the
# named balance is kept) to make the gold first, last or middle, whichever leaves |first| + |last| smallest; the
# row is then rendered again; when no set keeps the balance within RK_SLACK the unit is redrawn. Labels are
# unchanged (every candidate is a valid distractor; G2 / G3 re-solve the rows).
RANK_FORMS = ("C-VALUE", "C-PARAM")
# repair r9 (G6 choice b on build 20; tmp/t_kinds.py: qc C-TOOL gold written last among the options 70 / 617 rows vs
# sum 1/k 51.6, S2 rows showing the whole catalog 14 / 43 vs 7.0): C-TOOL rows join the worker's text-rank balance
# without a distractor swap (no unshown pool). Build 21 used the two-sided RK_SLACK rule and it redrew most middle-gold
# rows of large catalogs (their -1/k steps pushed |first| + |last| up; qc 20-60 bucket 374 -> 197 rows), so for
# RANK_ONLY forms only a gold written first / last is redrawn, when its own excess would pass RK_SLACK_ONLY.
RANK_ONLY = ("C-TOOL",)
RK_SLACK_ONLY = 1.0
RK = collections.defaultdict(lambda: [0.0, 0.0])  # key (form, gold named in the conversation y / n, "-" for C-VALUE)
RK_SLACK = 1.0  # a unit that would leave |first| + |last| above this and above its current value is redrawn
# gen:F12 after build 22 (G6 yes/no view d GBT .5255 vs chance .5023 + 2 pp; tmp/t_ynd2.log: dropping the request
# cue / statement-type features takes it to .4857): the outcome behind a yes/no label followed the visible structure
# (value statement present, request cue; G0 8 G6 features "request kind cue", "number of needed params"), so framing x
# structure predicted the label (tmp/t_ynorc.py: Y-ASK P / no value / plain cue 39 no vs 2 yes). Worker-level balance
# per cell (form, framing, value statement present, request cue): a yes/no unit whose rows would push |yes - no| of a
# cell above YS_SLACK and above its current value is redrawn. T-ATTACK / T-INERT / T-SOURCE rows and whole T-KIND units
# (quota twins whose structure the spec fixes: G0 4 T-KIND = polite request vs catalog question naming no entity or
# value) are counted but never cause a redraw (tmp/t_ysemu.py: GBT +0.8 pp over chance); the other label-flip twins
# keep the base's structure (f12extra._has_val), so a pair unit is neutral.
YS = collections.defaultdict(int)
YS_SLACK = 2
YS_EXEMPT = ("T-KIND", "T-ATTACK", "T-INERT", "T-SOURCE")


def ys_key(side):
    """(form, framing, value statement present, request cue) of a yes/no row, as qc/chk_lib.meta_feats reads them."""
    if side.get("form") not in YN_FORMS:
        return None
    conv = (side.get("S") or {}).get("conv") or []
    sts = [st for t in conv for st in (t.get("st") or []) if isinstance(st, dict)]
    cue = "+".join(sorted({str(st.get("cue")) for st in sts if st.get("t") == "req"}))
    return side.get("form"), str(side.get("framing")), any(st.get("t") == "val" for st in sts), cue


def _fpos(state, o):
    if len(o) < 2:
        return -1
    m = re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", state)
    return m.start() if m else -1


def rank_inc(state, texts, gold_text):
    pos = [_fpos(state, t) for t in texts]
    ok = sorted(x for x in pos if x >= 0)
    if len(ok) < 2:
        return 0.0, 0.0
    g = pos[texts.index(gold_text)]
    k = len(texts)
    return (1.0 if g == ok[0] else 0.0) - 1.0 / k, (1.0 if g == ok[-1] else 0.0) - 1.0 / k


def rank_key(form, gold_canon, S):
    """repair r8 (build 19: C-PARAM d excess 9.5 -> 4.5 without either "named" or "first / last"): the C-PARAM rank
    balance is kept separately for named and unnamed golds (abstain golds count as unnamed)."""
    if form != "C-PARAM":
        return (form, "-")
    g = list(gold_canon or [])
    return (form, "y" if len(g) > 1 and g[0] == "param" and g[1] in F.conv_named(S or {}) else "n")


def rank_note(row, side, form):
    if (form in RANK_FORMS or form in RANK_ONLY) and row.get("options"):
        a, b = rank_inc(row["state"], row["options"], row["gold"])
        key = rank_key(form, side.get("gold_canon"), side.get("S"))
        RK[key][0] += a
        RK[key][1] += b


def rank_fix(RR, card, state, rng):
    """Swap shown distractors for unshown ones (same class) to balance the gold's text rank; True if opts changed."""
    form, g, opts = RR["form"], RR["gold"], RR["opts"]
    card_r = dict(card)
    card_r["names"] = card.get("_names")
    tx = {}

    def t(o):
        if o not in tx:
            tx[o] = RD.opt_text(o, RR, card_r)
        return tx[o]
    if g[0] not in ("value", "param"):
        return False
    pg = _fpos(state, t(g))
    if pg < 0:
        return False
    cur = [o for o in opts if o != g and o[0] == g[0]]
    acat = RR.get("alt_cat")
    cat = (lambda o: acat.get(o[1], "n")) if acat else (lambda o: "-")  # noqa: E731
    cands = cur + [tuple(o) for o in RR["alt"] if tuple(o) not in cur and tuple(o) != g]
    P = {o: _fpos(state, t(o)) for o in cands}
    if form == "C-VALUE":
        if any(P[o] < 0 for o in cur):
            return False
        cands = [o for o in cands if P[o] >= 0]
    need = collections.Counter(cat(o) for o in cur)
    bef = lambda o: 0 <= P[o] < pg  # noqa: E731
    aft = lambda o: P[o] > pg  # noqa: E731

    def build(cls):
        out = []
        for c, n in need.items():
            lst = [o for o in cands if cat(o) == c]
            ok_ = [o for o in lst if not bef(o)] if cls == "first" else (
                [o for o in lst if not aft(o)] if cls == "last" else lst)
            if len(ok_) < n:
                return None
            out += ok_[:n]
        if cls == "mid":
            for want, other in ((bef, aft), (aft, bef)):
                if any(want(o) for o in out):
                    continue
                done = False
                for a in cands:
                    if a in out or not want(a):
                        continue
                    for i, o in enumerate(out):
                        if cat(o) == cat(a) and not (other(o) and sum(other(x) for x in out) == 1):
                            out[i] = a
                            done = True
                            break
                    if done:
                        break
                if not done:
                    return None
        return out
    rest = [o for o in opts if o not in cur]
    st = RK[rank_key(form, g, RR["S"])]
    best = None
    for cls in ("keep", "first", "last", "mid"):
        new = cur if cls == "keep" else build(cls)
        if new is None:
            continue
        a, b = rank_inc(state, [t(o) for o in new + rest], t(g))
        sc = (round(abs(st[0] + a) + abs(st[1] + b), 9), cls != "keep", rng.random())
        if best is None or sc < best[0]:
            best = (sc, new)
    if best[0][0] > max(abs(st[0]) + abs(st[1]), RK_SLACK) + 1e-9:
        raise SM.Reject(f"{form} rank balance")  # no distractor set keeps the balance: redraw the unit
    new = best[1]
    if set(new) == set(cur):
        return False
    keep = [o for o in cur if o in new]
    add = [o for o in new if o not in cur]
    it = iter(add)
    RR["opts"] = [o if (o not in cur or o in keep) else next(it) for o in opts]
    return True


def cv_text_check(row, opts):
    """repair r2 (G6 / G7): the value options of a C-VALUE row are all written in `state` or none is (f12forms.c_value);
    the rendered row is checked with whole-token matching, and a row that breaks it is rejected and redrawn."""
    vals = [o for o, c in zip(row["options"], opts) if c[0] == "value"]
    ins = {bool(re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", row["state"])) for o in vals if len(o) >= 2}
    if len(ins) > 1:
        raise SM.Reject("C-VALUE mixed in-text class")


def build_card(card, cards, mode, n_rows, seed, held_out=False):
    pk = next(p for p in packs() if p["id"] == card["pack"])
    rng = random.Random(f"{seed}-{card['id']}-{mode}")
    card["_names"] = card_names(card, pk)
    ctx = SM.Ctx(pk, card["_tools"], card, rng, borrow_pool(card, cards))
    ctx.bal = F.Bal(rng)
    styles = styles_for(held_out)
    cr = random.Random("styles-" + card["id"])
    st_pool = cr.sample(styles, min(12, len(styles)))
    rows, sides, rels = [], [], []
    picker = FormPicker(card, rng)
    u = 0
    made = 0
    fails = {}
    for _ in range(4 * n_rows):
        if made >= n_rows:
            break
        form = picker.next()
        if form is None:
            break
        try:
            cfw = cf_want(card, form, rng)
            if form in F.BUILDERS:
                R = F.BUILDERS[form](ctx, rng, cfw)
            elif form in ("Y-CALLX", "Y-ASK", "Y-FIT", "Y-DIRECT"):
                R = F.yes_no(ctx, rng, form, cfw)
            elif form in EXTRA:
                R = EXTRA[form](ctx, rng, {})
            else:
                continue
            if EXTRA_TWINS and card["sampler"] in ("S1", "S2", "S4", "S6") and form != "C-INV":
                EXTRA_TWINS(ctx, R, rng)
                if R.get("twins"):  # a label-flip twin may not push its gold kind above the card's target (G10)
                    R["twins"] = [x for x in R["twins"] if not (x[2] is None and twin_over(ctx, R, x[0]))] or None
            if R.get("yn_intent"):  # repair r9 (f12forms.PAIR_SHARE): pair units need a label-flip twin; singles none
                flips = [x for x in (R.get("twins") or []) if x[2] is None]
                if R["yn_intent"] == "pair":
                    F.bal(ctx).yn_try(form, R["framing"], R["gold"], bool(flips))
                    if not flips:
                        raise SM.Reject("yn pair: no label-flip twin")
                else:
                    R["twins"] = [x for x in (R.get("twins") or []) if x[2] is not None] or None
        except (SM.Reject, AssertionError) as e:
            fails[str(e)[:50]] = fails.get(str(e)[:50], 0) + 1
            picker.fail[form] += 1
            continue
        u += 1
        prepare_texts(R, pk, rng)
        unit = [(R, 0, None, None)]
        if R["qtype"] == "noul" and rng.random() < P_NEG and made + 3 <= n_rows:
            unit = [(R, 0, None, None), (R, 1, "complement", "T-NEG"), (R, 2, "equiv", "T-NEG2")]
        # a label-flip / attack / inert twin rides along (own call_id for label-flip twins, so the relation unit of
        # the T-NEG rows stays <= 3 rows)
        if R.get("yn_intent") == "pair" and not (made + len(unit) + len(R["twins"]) <= n_rows and (
                len(unit) == 1 or all(rel is None for _, _, rel in R["twins"]))):  # repair r9: a pair keeps its twin
            fails["yn pair: no room"] = fails.get("yn pair: no room", 0) + 1
            picker.fail[form] += 1
            continue
        if R.get("twins") and made + len(unit) + len(R["twins"]) <= n_rows and \
                (len(unit) == 1 or all(rel is None for _, _, rel in R["twins"])):
            for R2, tk, rel in R["twins"]:
                share_texts(R, R2)
                prepare_texts(R2, pk, rng)
                unit.append((R2, 0, rel, tk))
        # not-generated structures on any row of the unit, twins included (G0 10.1: NG-29, NG-55; fixA pass 1)
        try:
            ngbad = any(RR.get("res") and RR["S"].get("conv") and RR.get("form") != "C-INV" and
                        (SM.ng29_bad(RR["S"], RR["res"], pk) or SM.ng55_bad(RR["S"], pk)) for RR, _, _, _ in unit)
        except AssertionError:
            ngbad = True
        if ngbad:
            fails["NG-29/NG-55 unit"] = fails.get("NG-29/NG-55 unit", 0) + 1
            picker.fail[form] += 1
            continue
        # the unit shares one card mode: every row of it must be card_free_ok; T-KIND sets and attack units never are
        cf0 = card_free_ok(R, ctx.pk)
        cfree = cf0 and not (card["_names"] and form in NAMED_FORMS) and all(
            tk not in ("T-KIND", "T-ATTACK") and (rel is not None or card_free_ok(RR, ctx.pk))
            for RR, _, rel, tk in unit[1:])
        CF_STATS[(card["sampler"], bool(cfw.get("cf")), cf0, cfree)] += 1
        cm = "full"
        if cfree and rng.random() < P_SHORT and short_ok(card, form, unit):
            cm = rng.choice(["short", "none"])
        style = rng.choice(st_pool)
        wid = wording_for(card, form, rng)
        base_id = f"f12-{mode}-{card['id']}-u{u:04d}"
        ok_unit = []
        try:
            for j, (RR, neg, rel, tk) in enumerate(unit):
                rid = base_id + "abcdef"[j]
                own_call = j > 0 and rel is None
                f, texts, gold, q, ir, ms = render_row(RR, card, pk, style["id"], wid, mode, rid, neg=neg,
                                                       card_mode=cm)
                if j == 0 and len(unit) == 1 and form in RANK_FORMS and RR.get("alt") is not None and \
                        rank_fix(RR, card, f["state"], rng):  # repair r8
                    f, texts, gold, q, ir, ms = render_row(RR, card, pk, style["id"], wid, mode, rid, neg=neg,
                                                           card_mode=cm)
                row = {"id": rid, "group_id": "f12_g_" + base_id[4:],
                       "call_id": "f12_c_" + (rid if own_call else base_id + "a"),
                       "source": "c_f12", "state": f["state"], "qtype": RR["qtype"], "instructions": f["instructions"],
                       "options": texts, "gold": gold, "role": "own", "card": f["card"],
                       "meta": {"family": FAM, "spec_id": SPEC_ID, "card_id": card["id"], "domain_pack": card["pack"],
                                "sampler": card["sampler"], "gen_version": GEN_VERSION, "git_sha": "unknown",
                                "seed": rng.randrange(1 << 30), "structure_hash": structure_hash(RR, card),
                                "difficulty_bin": None, "crowd_pg": None, "depth": depth_of(RR),
                                "deep": depth_of(RR) >= 4, "format_style": style["id"], "wording_id": wid,
                                "defs_style": card["defs_style"] if cm == "full" else ("short" if cm == "short"
                                                                                         else "no_card"),
                                "twin_of": None if j == 0 else base_id + "a",
                                "twin_kind": tk,
                                "text_source": None, "licence": LICENCE, "edge": [], "subtype": form,
                                "persona_seed": card["persona_seed"]}}
                if form == "C-VALUE":
                    cv_text_check(row, RR["opts"])
                tok = served_tokens(row)
                if tok > TOKEN_CAP:
                    raise SM.Reject("token cap")
                side = {"id": rid, "card": card["id"], "form": form, "framing": RR.get("framing"), "neg": neg,
                        "outcome": RR["res"]["outcome"] if RR.get("res") else None,
                        "kind": RR["res"]["kind"] if RR.get("res") else None,
                        "tool": RR["res"].get("tool") if RR.get("res") else None,
                        "near_miss": [list(x) for x in RR.get("nm") or []], "card_mode": cm,
                        "card_free_ok": cfree, "gold_canon": list(RR["gold"]) if isinstance(RR["gold"], tuple)
                        else RR["gold"], "opts_canon": [list(o) for o in RR["opts"]] if RR["opts"] else None,
                        "q": RR["q"], "question": q, "layout": "compact" if len(RR["S"]["tools"]) >= 26 else "full",
                        "catalog_n": len(RR["S"]["tools"]), "real_tokens": tok, "names": card["_names"],
                        "S": strip(RR["S"]), "cases": RR.get("cases_struct"), "must_show": ms,
                        "audit": RR.get("audit"), "twin_kind": tk, "rel": rel}
                ok_unit.append((row, side, rel))
        except (fcard.FormatError, SM.Reject, AssertionError) as e:
            fails["render:" + str(e)[:40]] = fails.get("render:" + str(e)[:40], 0) + 1
            picker.fail[form] += 1
            continue
        # repair r8: a multi-row unit (twins; rank_fix only swaps on single rows) is redrawn when its rows would push
        # the worker's text-rank balance above RK_SLACK and above its current value
        if form in RANK_ONLY:  # repair r9: one-sided cap on gold first / last over 1/k
            inc = collections.defaultdict(lambda: [0.0, 0.0])
            for rw, sd, _ in ok_unit:
                if rw.get("options"):
                    x, y = rank_inc(rw["state"], rw["options"], rw["gold"])
                    kk = rank_key(form, sd.get("gold_canon"), sd.get("S"))
                    inc[kk][0] += x
                    inc[kk][1] += y
            if any((x > 0 and RK[kk][0] + x > RK_SLACK_ONLY) or (y > 0 and RK[kk][1] + y > RK_SLACK_ONLY)
                   for kk, (x, y) in inc.items()):
                fails["rank cap unit"] = fails.get("rank cap unit", 0) + 1
                picker.fail[form] += 1
                continue
        if form in RANK_FORMS and len(ok_unit) > 1:
            inc = collections.defaultdict(lambda: [0.0, 0.0])
            for rw, sd, _ in ok_unit:
                if rw.get("options"):
                    x, y = rank_inc(rw["state"], rw["options"], rw["gold"])
                    kk = rank_key(form, sd.get("gold_canon"), sd.get("S"))
                    inc[kk][0] += x
                    inc[kk][1] += y
            if any(abs(RK[kk][0] + x) + abs(RK[kk][1] + y) > max(abs(RK[kk][0]) + abs(RK[kk][1]), RK_SLACK) + 1e-9
                   for kk, (x, y) in inc.items()):
                fails["rank balance unit"] = fails.get("rank balance unit", 0) + 1
                picker.fail[form] += 1
                continue
        # relation units (rows sharing the base call_id) with any row >= 2,000 tokens hold at most 2 rows (2.1)
        rel_rows = [x for x in ok_unit if x[0]["call_id"] == ok_unit[0][0]["call_id"]]
        if len(rel_rows) == 3 and max(s["real_tokens"] for _, s, _ in rel_rows) >= 2000:
            drop = rel_rows[2] if rng.random() < 0.55 else rel_rows[1]
            ok_unit = [x for x in ok_unit if x is not drop]
        if form in YN_FORMS and not any(sd.get("twin_kind") == "T-KIND" for _, sd, _ in ok_unit):  # see YS
            inc = collections.defaultdict(int)
            for rw, sd, _ in ok_unit:
                k = ys_key(sd)
                if k is not None and sd.get("twin_kind") not in YS_EXEMPT:
                    inc[k] += 1 if int(rw["gold"]) else -1
            if any(abs(YS[k] + x) > max(abs(YS[k]), YS_SLACK) for k, x in inc.items()):
                fails["yn struct unit"] = fails.get("yn struct unit", 0) + 1
                picker.fail[form] += 1
                continue
        if form in YN_FORMS:
            for rw, sd, _ in ok_unit:
                k = ys_key(sd)
                if k is not None:
                    YS[k] += 1 if int(rw["gold"]) else -1
        for row, side, rel in ok_unit:
            bal_update(ctx, card, side, row)
            rank_note(row, side, form)  # repair r8
            short_update(card, form, side, row)
            rows.append(row)
            sides.append(side)
            if rel:
                rels.append({"a": base_id + "a", "b": row["id"], "type": rel})
        if R.get("yn_intent"):  # repair r9: pair share per card and form
            F.bal(ctx).yn_done(form, R["yn_intent"] == "pair" and any(
                sd.get("twin_kind") and rl is None for _, sd, rl in ok_unit[1:]))
        made += len(ok_unit)
        picker.made[form] += len(ok_unit)
    return rows, sides, rels, fails


def strip(S):
    S = copy.deepcopy(S)
    for t in S["tools"]:
        for k in list(t):
            if k in ("compact",):
                t.pop(k)
    return S


EXTRA = {}
EXTRA_TOOLS = {}
EXTRA_TWINS = None
CDEF_RECORD = None
EXTRA_EXAMPLES = None


def packs_tools(pk):
    """The fixed tool set of the card that owns pack pk (G4 MR4 inert supply)."""
    cards, s5 = plan_cards() if "_PLAN" not in globals() else globals()["_PLAN"]
    globals()["_PLAN"] = (cards, s5)
    for c in cards + s5:
        if c["pack"] == pk["id"]:
            return c["_tools"]
    return []


def main():
    mode = sys.argv[1]
    shard = (0, 1)
    if "--shard" in sys.argv:
        a, b = sys.argv[sys.argv.index("--shard") + 1].split("/")
        shard = (int(a), int(b))
    only = sys.argv[sys.argv.index("--cards") + 1].split(",") if "--cards" in sys.argv else None
    cards, s5 = plan_cards()
    PARTS.mkdir(parents=True, exist_ok=True)
    if mode == "dev":
        todo = [(c, 400 // len(s5) + (1 if i < 400 % len(s5) else 0)) for i, c in enumerate(s5)]
    else:
        tot = {}
        for c in cards:
            tot[c["sampler"]] = tot.get(c["sampler"], 0) + 1
        mult = 1.5 if mode == "cand" else QC_ROWS / 2700
        todo = [(c, int(round(C.ROWS_R1[c["sampler"]] * mult / tot[c["sampler"]]))) for c in cards]
    todo = [t for i, t in enumerate(todo) if i % shard[1] == shard[0] and (not only or t[0]["id"] in only)]
    tag = f"{mode}_{shard[0]}of{shard[1]}"
    with open(PARTS / f"{tag}.jsonl", "w") as fr, open(PARTS / f"{tag}.side.jsonl", "w") as fs, \
            open(PARTS / f"{tag}.rel.jsonl", "w") as fl:
        for card, n in todo:
            if card["sampler"] in ("S3",) and "S3" not in EXTRA_SAMPLERS:
                log(f"{tag} skip {card['id']} (S3 builder not loaded)")
                continue
            t0 = time.time()
            rows, sides, rels, fails = build_card(card, cards, mode, n, SEED + (0 if mode == "cand" else 7919),
                                                  held_out=card["sampler"] == "S5")
            for r in rows:
                fr.write(json.dumps(r, default=str) + "\n")
            for s in sides:
                fs.write(json.dumps(s, default=str) + "\n")
            for r in rels:
                fl.write(json.dumps(r) + "\n")
            fr.flush()
            log(f"{tag} {card['id']} rows {len(rows)}/{n} {time.time() - t0:.0f}s top-fails "
                f"{sorted(fails.items(), key=lambda x: -x[1])[:3]}")
    with open(PARTS / f"{tag}.done", "w") as f:
        f.write("done\n")


EXTRA_SAMPLERS = set()
try:  # S3 audit and C-INV / S5 builders plug in here when present
    import f12extra  # noqa: E402
    EXTRA.update(f12extra.BUILDERS)
    EXTRA_SAMPLERS |= set(f12extra.SAMPLERS)
    EXTRA_TOOLS.update(getattr(f12extra, "TOOLS", {}))
    EXTRA_TWINS = f12extra.add_twins
    CDEF_RECORD = f12extra.cdef_record
    EXTRA_EXAMPLES = f12extra.card_examples
except ImportError:
    pass

if __name__ == "__main__":
    main()
