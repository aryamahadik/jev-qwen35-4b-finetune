"""F8 renderer: structure S + card + row choices -> raw row fields through formats-1 (card.render_row_text).

Choice rows follow ruling A16.1 (g) (G0 spec 1 choice-row layout): rules, SEM lines, tables and examples are card
blocks that fmt1 moves into `instructions`; `card` holds only '- <option>: <definition>' lines (DEC action meanings,
masked PRED codes) or is null; case data are `state`. Yes/no rows print the card whole.
"""
from __future__ import annotations

from fractions import Fraction as Fr

import facts as FT
import lexicon as L
from fmt1 import card as fcard
from fmt1 import pool as fpool
from fmt1.render import FormatError
from numfmt import chance_text, money_text, num_text, points_text
from semsets import sem_set

# ------------------------------------------------------------------------------------------------ words
def item_words(card: dict) -> tuple:
    if card["schema"] == "dec" or card.get("q", {}).get("k") == "tec":
        return "action", "actions"
    return card["case"]["noun"], card["case"]["plural"]


def qname(card: dict, q: dict) -> str:
    k = q["k"]
    if k == "risk":
        return "risk"
    if k == "score":
        return "score"
    if k == "el":
        return "expected loss"
    if k == "tec":
        return "total expected cost"
    if k == "ev":
        return "expected value"
    if k == "en":
        return f"expected number of '{card['events'][0]}'"
    if k == "chance":
        return f"chance of '{card['events'][0]}'"
    if k == "post":
        return "chance"
    raise ValueError(k)


def qdef_text(card: dict, d: str) -> str:
    return {"el": "expected loss", "score": "score", "chance": f"chance of '{card['events'][0]}'",
            "tec": "total expected cost"}[d]


def sem_text(card: dict, key: str) -> str:
    v = card["sem_variant"].get(key, 0)
    t = L.SEM[key][min(v, len(L.SEM[key]) - 1)]
    io, ios = item_words(card)
    q = card.get("q", {})
    fill = {"case": card["case"]["noun"], "cases": card["case"]["plural"], "document": card["doc_word"],
            "option": io, "options": ios, "idnum": "reference number", "unit": card["cur"]["plural"],
            "CBD": L.CBD, "NOTA": L.NOTA, "source": "figures given", "E": "the sign",
            "event": (card.get("events") or ["the event"])[0],
            "units": (card.get("units") or ("unit", "units"))[1]}
    if card["rules"].get("scorecard"):
        fill["F"] = card["rules"]["scorecard"]["F"]
        fill["M"] = card["rules"]["scorecard"]["M"]
    if key == "SEM-12":
        fill["quantity"] = qname(card, q) if q.get("k") != "risk" else "risk"
    if key == "SEM-22":
        fill["qdef"] = qdef_text(card, q["def"])
    if key == "SEM-25":
        m = card["rules"]["mat"]
        fill["impact_def"] = (f"the loss if '{fill['event']}' happens" if m["impact"] == "loss"
                              else f"the expected loss of the {card['case']['noun']} (chance x loss)")
    return t.format(**{k: v for k, v in fill.items()})


# ------------------------------------------------------------------------------------------------ conditions
def chance_t(p: Fr, rep: str = "pct0", den=None) -> str:
    return chance_text(p, rep, den)


def cmp_word_for(op: str, idx: int = 0, *, neg: bool = False) -> str:
    ws = [w["w"] for w in L.COMPARATORS[op] if (w["neg_ok"] or not neg)]
    return ws[idx % len(ws)]


def part_text(part: dict, card: dict) -> str:
    t = part["t"]
    if t == "bool":
        return f"it shows '{part['f']}'"
    if t == "cat":
        return f"its {part['name']} is '{part['v']}'"
    if t == "amt":
        return f"its {part['name']} is {part['w']} {money_text(part['v'], card['cur'])}"
    if t == "q":
        qq = part["q"]
        w = part["w"]
        if qq["k"] == "score":
            return f"its score is {w} {part['v'].numerator}"
        if qq["k"] in ("el", "tec", "ev"):
            return f"its {qname(card, qq)} is {w} {money_text(part['v'], card['cur'])}"
        if qq["k"] in ("chance",):
            return f"its {qname(card, qq)} is {w} {chance_text(part['v'], 'pct0')}"
        raise ValueError(qq)
    raise ValueError(t)


def cond_text(cond: dict, card: dict) -> str:
    ps = [part_text(p, card) for p in cond["parts"]]
    conn = cond["conn"]
    if len(ps) == 1:
        return ps[0]
    if conn == "xor1":
        head = "exactly one of "
        return head + (" and ".join(ps) if len(ps) == 2 else f"{ps[0]}, {ps[1]} and {ps[2]}")
    j = " and " if conn == "and" else " or "
    if len(ps) == 2:
        return ps[0] + j + ps[1]
    return f"{ps[0]}, {ps[1]}{j}{ps[2]}"


def cap1(s: str) -> str:
    return s[:1].upper() + s[1:]


def line_text(ln: dict, card: dict) -> str:
    s = cap1(cond_text(ln["cond"], card)) + ": " + points_text(ln["pts"])
    if ln.get("unless"):
        s += ", unless " + cond_text(ln["unless"], card)
    return s + "."


def cut_range(cuts: list, i: int) -> str:
    if i == 0:
        return f"below {cuts[0]}"
    if i == len(cuts):
        return f"at least {cuts[-1]}"
    return f"at least {cuts[i - 1]} and below {cuts[i]}"


def bin_range(edges: list, conv: str, i: int) -> str:
    def pc(x):
        return chance_text(x, "pct0") if (x * 100).denominator == 1 else chance_text(x, "pct1")
    lo = Fr(0) if i == 0 else edges[i - 1]
    hi = Fr(1) if i == len(edges) else edges[i]
    if conv == "lo":
        if i == len(edges):
            return f"at least {pc(lo)} and at most 100%"
        return f"at least {pc(lo)} and below {pc(hi)}"
    if i == 0:
        return f"at least 0% and at most {pc(hi)}"
    return f"above {pc(lo)} and at most {pc(hi)}"


def money_range(edges: list, i: int, cur: dict) -> str:
    if i == 0:
        return f"below {money_text(edges[0], cur)}"
    if i == len(edges):
        return f"at least {money_text(edges[-1], cur)}"
    return f"at least {money_text(edges[i - 1], cur)} and below {money_text(edges[i], cur)}"


# ------------------------------------------------------------------------------------------------ card IR
def rule_blocks(card: dict, version: str) -> list:
    R = card["rules"]
    reg = "Rules"
    blocks = []
    sc = R.get("scorecard")
    if sc:
        items = [line_text(ln, card) for ln in sc["lines"]]
        items.append(f"The score floor is {sc['F']} and the score cap is {sc['M']}.")
        blocks.append({"type": "section", "heading": "Scorecard",
                       "blocks": [{"type": "steps" if card["defs_style"] == "decision_list" else "items",
                                   "items": items}]})
    if card["schema"] == "tier":
        tiers = R["tiers"]
        rows = [[t, cut_range(R["cuts"], i)] for i, t in enumerate(tiers)]
        blocks.append({"type": "table", "caption": "Tiers, lowest to highest", "columns": ["Tier", "Score range"],
                       "rows": rows})
        lim = [f"Tier '{tiers[int(t)]}' only if {cond_text(c, card)}." for t, c in sorted(R["only_if"].items())]
        ov = [f"Override: if {cond_text(o['cond'], card)}, the tier is '{tiers[o['tier']]}'." for o in R["overrides"]]
        blocks.append({"type": "section", "heading": "Tier limits and overrides",
                       "blocks": [{"type": "items", "items": lim + ov}]})
    if R.get("arules"):
        items = [f"'{a}' is required when {cond_text(c, card)}." for a, c in R["arules"].items()]
        blocks.append({"type": "section", "heading": "Action rules", "blocks": [{"type": "items", "items": items}]})
    if card["schema"] == "inv":
        r = R["inv"]
        if r["kind"] == "act":
            txt = f"The rule: a {card['case']['noun']} meets the rule when it requires '{r['action']}'."
        else:
            part = {"t": "q", "q": r["q"], "op": r["op"], "v": r["v"], "w": r["w"]}
            txt = f"The rule: a {card['case']['noun']} meets the rule when {part_text(part, card)}."
        blocks.append({"type": "para", "text": txt})
    if card["schema"] == "mat":
        m = R["mat"]
        ev = card["events"][0]
        lrows = [[n, bin_range(m["lik_edges"], m["lik_conv"], i)] for i, n in enumerate(m["lik_names"])]
        irows = [[n, money_range(m["imp_edges"], i, card["cur"])] for i, n in enumerate(m["imp_names"])]
        grid = [[m["lik_names"][i]] + [m["ratings"][x] for x in row] for i, row in enumerate(m["grid"])]
        blocks.append({"type": "table", "caption": "Likelihood levels", "columns": ["Likelihood level",
                                                                                   f"Chance of '{ev}'"], "rows": lrows})
        blocks.append({"type": "table", "caption": "Impact levels",
                       "columns": ["Impact level", "Loss" if m["impact"] == "loss" else "Expected loss"],
                       "rows": irows})
        blocks.append({"type": "table", "caption": "Rating grid", "columns": ["Likelihood level"] + m["imp_names"],
                       "rows": grid})
        blocks.append({"type": "para", "text": "Ratings from lowest to highest: " +
                       ", ".join(f"'{x}'" for x in m["ratings"]) + "."})
    return blocks


def sem_blocks(card: dict, version: str) -> list:
    keys = sem_set(card, version)
    lines = [sem_text(card, k) for k in keys]
    if not lines:
        return []
    kind = "steps" if card["defs_style"] == "decision_list" else "items"
    return [{"type": "section", "heading": "Reading rules", "blocks": [{"type": kind, "items": lines}]}]


def card_ir(card: dict, version: str, examples: list | None = None) -> dict | None:
    if version == "none":
        return None
    blocks = sem_blocks(card, version) + rule_blocks(card, version)
    if examples and version == "full":
        blocks.append({"type": "fewshot", "template": card["fewshot_template"], "heading": None,
                       "examples": [{"case": e["case"], "answer": e["answer"]} for e in examples]})
    return {"title": None, "blocks": blocks}


def option_defs(card: dict, options: list) -> list:
    """'- <option>: <definition>' entries (choice rows only): DEC action meanings and masked PRED codes."""
    out = []
    if card["schema"] == "dec":
        dmap = {a["label"]: a.get("defn") for a in card["actions"]}
        for o in options:
            if dmap.get(o):
                out.append({"name": o, "text": dmap[o]})
    if card["schema"] == "pred" and card.get("hyp_defs"):
        for o in options:
            if o in card["hyp_defs"]:
                out.append({"name": o, "text": f"outcome '{card['hyp_defs'][o]}'"})
    return out


# ------------------------------------------------------------------------------------------------ facts (state)
def S_(key: str, var: int, **kw) -> str:
    vs = FT.SENT[key]
    return vs[var % len(vs)].format(**kw)


def chance_of(v, rep, den):
    return chance_text(v, rep, den)


def ent_facts(card: dict, S: dict, e: dict, var: int, *, fields: bool) -> tuple:
    """(sentences, field pairs) for one entity. fields=True puts case attributes in key-value pairs (S2)."""
    sents, pairs = [], []
    cur = card["cur"]
    ID = e["id"]
    kw = {"ID": ID, "case": card["case"]["noun"], "cases": card["case"]["plural"]}
    if fields:
        pairs.append(["Reference", ID])
    if "pts" in e:
        pts = e["pts"]
        for f, val in pts["b"].items():
            if not pts["stated"].get(f, True):
                continue
            if fields:
                pairs.append([f, "not recorded" if val is None else ("yes" if val else "no")])
            elif val is None:
                sents.append(S_("f_nr", var, F=f, **kw))
            else:
                sents.append(S_("f_yes" if val else "f_no", var, F=f, **kw))
        for c, val in pts["c"].items():
            if fields:
                pairs.append([c, val])
            else:
                sents.append(S_("cat", var, cat=c, v=val, **kw))
        for a, val in pts["a"].items():
            if fields:
                pairs.append([a, money_text(val, cur) if val is not None else "not recorded"])
            elif val is None:
                sents.append(S_("amt_nr", var, amtname=a, **kw))
                lo, hi = pts["arng"][a]
                sents.append(S_("amt_rng", var, amtname=a, lo=money_text(lo, cur), hi=money_text(hi, cur), **kw))
            else:
                sents.append(S_("amt", var, amtname=a, money=money_text(val, cur), **kw))
    if "bay" in e:
        bay = e["bay"]
        rep = bay.get("rep", {})
        sign = bay["signs"]
        if bay["form"] == "rates":
            for j, h in enumerate(bay["hyps"]):
                sents.append(S_("base", var, p=chance_of(bay["base"][j], rep["base"], rep["base_den"]), H=h, **kw))
            for s in sign:
                for j, h in enumerate(bay["hyps"]):
                    v = bay["lik"][s][j]
                    if v is None:
                        sents.append(S_("lik_nr", var, H=h, E=s, **kw))
                        lo, hi = bay["rng"][f"{s}|{j}"]
                        if bay.get("rngshow", {}).get(f"{s}|{j}"):
                            sents.append(S_("lik_rng", var, H=h, E=s, lo=chance_text(lo, "pct0"),
                                            hi=chance_text(hi, "pct0"), **kw))
                    else:
                        den = rep["lik_den"][j] if isinstance(rep["lik_den"], list) else rep["lik_den"]
                        r_ = rep["lik"]
                        if rep.get("lik_list"):
                            r_, den = rep["lik_list"][j]
                        sents.append(S_("lik", var, p=chance_of(v, r_, den), H=h, E=s, **kw))
        elif bay["form"] == "joint":
            for s in sign:
                for j, h in enumerate(bay["hyps"]):
                    sents.append(S_("joint", var, p=chance_text(bay["joint"][s][j], "pct0"), H=h, E=s, **kw))
        elif bay["form"] == "counts" and not fields:
            if card["sampler"] != "S3":
                for s in sign:
                    for j, h in enumerate(bay["hyps"]):
                        a, b = bay["cnt"][s][j]
                        sents.append(S_("cnt", var, H=h, E=s, a=a, b=b, **kw))
        elif bay["form"] == "nE":
            for s in sign:
                n = sum(bay["ne"][s])
                key = "cnt_e" if bay["sig"][s] else "cnt_ne"
                for j, h in enumerate(bay["hyps"]):
                    sents.append(S_(key, var, H=h, E=s, a=bay["ne"][s][j], n=n, **kw))
        for s in sign:
            sents.append(S_("sig_yes" if bay["sig"][s] else "sig_no", var, E=s, **kw))
    if "outs" in e and e["outs"]:
        if e.get("action") is not None and card["schema"] == "dec":
            sents.append(S_("act", var, action=e["action"], **kw))
        net = "_net" if S.get("mode") == "net" else ""
        for o in e["outs"]:
            ev = o["ev"]
            if o["p"] is None:
                sents.append(S_("outp_nr" + net, var, event=ev, money=money_text(o["a"], cur), **kw))
                lo, hi = o["prng"]
                if o.get("prng_show"):
                    sents.append(S_("outp_rng", var, event=ev, lo=chance_text(lo, "pct0"), hi=chance_text(hi, "pct0"),
                                    **kw))
            elif o["a"] is None:
                sents.append(S_("outa_nr" + net, var, event=ev, p=chance_of(o["p"], o["prep"], o["pden"]), **kw))
                lo, hi = o["arng"]
                sents.append(S_("outa_rng" + net, var, event=ev, lo=money_text(lo, cur), hi=money_text(hi, cur),
                                **kw))
            else:
                key = "out_net" if S.get("mode") == "net" else "out"
                sents.append(S_(key, var, event=ev, p=chance_of(o["p"], o["prep"], o["pden"]),
                                money=money_text(o["a"], cur), **kw))
        if e.get("cost") is not None:
            ctext = e.get("cost_word") or money_text(e["cost"], cur)
            if e.get("cost_word") in ("0", "None"):
                ctext = e["cost_word"] if e["cost_word"] == "None" else money_text(Fr(0), cur)
            sents.append(S_("cost", var, money=ctext, **kw))
    if e.get("ch") is not None:
        ch = e["ch"]
        if ch["p"] is None:
            sents.append(S_("ch_nr", var, event=ch["ev"], **kw))
            lo, hi = ch["rng"]
            sents.append(S_("ch_rng", var, event=ch["ev"], lo=chance_text(lo, "pct0"), hi=chance_text(hi, "pct0"), **kw))
        else:
            sents.append(S_("ch", var, event=ch["ev"], p=chance_of(ch["p"], ch["rep"], ch["den"]), **kw))
        if ch.get("amt") is not None:
            sents.append(S_("loss", var, event=ch["ev"], money=money_text(ch["amt"], cur), **kw))
    if e.get("en") is not None:
        en = e["en"]
        sents.append(S_("en", var, n=en["n"], units=card["units"][1], event=en["ev"],
                        p=chance_of(en["p"], en["rep"], en["den"]), **kw))
    if e.get("mat") is not None:
        m = e["mat"]
        ev = card["events"][0]
        sents.append(S_("ch", var, event=ev, p=chance_of(m["lik"], m["rep"], m["den"]), **kw))
        sents.append(S_("loss", var, event=ev, money=money_text(m["amt"], cur), **kw))
    return sents, pairs


def counts_table(card: dict, e: dict) -> dict:
    bay = e["bay"]
    s = bay["signs"][0]
    rows = [[h, str(c[0]), str(c[1])] for h, c in zip(bay["hyps"], bay["cnt"][s])]
    return {"type": "table", "caption": None, "columns": FT.TABLE_COLS["counts"], "rows": rows}


def doc_parts(card: dict, S: dict, row: dict) -> dict:
    """Logical state content: title, preamble lines (no-card version), field groups, sentences, tables."""
    samp = card["sampler"]
    var = 1 if samp == "S4" else 0
    noun = card["case"]["noun"]
    pre = []
    if row["version"] == "none":
        pre = [sem_text(card, k) for k in sem_set(card, "none")]
        for b in rule_blocks(card, "none"):
            if b["type"] == "section":
                for bb in b["blocks"]:
                    pre += bb["items"]
            elif b["type"] == "para":
                pre.append(b["text"])
    ents = S["ents"]
    if S.get("case") is not None and S["form"] not in ("rank_top", "rank_order", "inv", "dec"):
        title = f"{cap1(card['doc_word'])} for {ents[S['case']]['id']}"
    else:
        title = f"{cap1(card['doc_word'])}: {card['case']['plural']}"
    if S["form"] == "dec":
        title = f"{cap1(card['doc_word'])}: actions for one {noun}"
    fields, sents, tables = [], [], []
    if samp == "S3" and S["form"] in ("rank_top", "rank_order", "inv"):
        tables.append(case_table(card, S))
        for e in ents:
            if e.get("ch") is not None and e["ch"]["p"] is None:
                lo, hi = e["ch"]["rng"]
                sents.append(S_("ch_rng", 0, ID=e["id"], event=e["ch"]["ev"], lo=chance_text(lo, "pct0"),
                                hi=chance_text(hi, "pct0")))
            for o in e.get("outs") or []:
                if o["p"] is None:
                    lo, hi = o["prng"]
                    sents.append(S_("outp_rng", 0, ID=e["id"], event=o["ev"], lo=chance_text(lo, "pct0"),
                                    hi=chance_text(hi, "pct0")))

    else:
        for e in ents:
            fs, pairs = ent_facts(card, S, e, var, fields=(samp == "S2" and "pts" in e))
            if pairs:
                lab = "Case details" if len(ents) == 1 else f"Case details {e['id']}"
                fields.append((lab, pairs))
            sents += fs
            if e.get("bay", {}).get("form") == "counts" and samp == "S3":
                tables.append(counts_table(card, e))
                sents.insert(0, S_("cnt_cap", 0, E=e["bay"]["signs"][0], cases=card["case"]["plural"]))
    if row.get("inert"):
        pos = row.get("inert_pos", 0) % (len(sents) + 1)
        sents.insert(pos, row["inert"])
    return {"title": title, "pre": pre, "fields": fields, "sents": sents, "tables": tables, "var": var}


def doc_ir(card: dict, S: dict, row: dict, container: str, skin: str, people: list) -> dict:
    """The state Doc for one row in one container (8.1-8.4)."""
    D = doc_parts(card, S, row)
    samp = card["sampler"]
    blocks = []
    if container == "email_thread" and skin != "email.single":
        msgs = []
        sp = people or ["Reviewer"]
        if D["pre"]:
            msgs.append({"speaker": sp[0], "text": "\n".join(D["pre"])})
        if D["fields"] or D["tables"]:
            raise FormatError("email threads carry sentences only")
        if D["sents"]:
            half = max(1, len(D["sents"]) // 2) if len(D["sents"]) >= 4 else len(D["sents"])
            msgs.append({"speaker": sp[1 % len(sp)], "text": " ".join(D["sents"][:half])})
            if D["sents"][half:]:
                msgs.append({"speaker": sp[2 % len(sp)], "text": " ".join(D["sents"][half:])})
        if skin == "email.list_archive":
            for m in msgs:
                m["subject"] = D["title"]
        return {"title": D["title"], "blocks": [{"type": "messages", "messages": msgs}]}
    if D["pre"]:
        blocks.append({"type": "section", "heading": "Reading rules",
                       "blocks": [{"type": "items", "items": D["pre"]}]})
    if samp == "S5" and not D["fields"]:
        # held-out shape (8.5): an indented outline; branches by class or by option, sentences as leaves
        import re as _re
        groups = {}
        for x in D["sents"]:
            m = _re.search(r"classed '([^']+)'", x)
            if m:
                key = f"Branch: class '{m.group(1)}'"
            else:
                m = _re.search(r"\b([A-Z]{2,4}-\d{2,4})\b", x)
                key = f"Branch: {m.group(1)}" if m else "Other facts"
            groups.setdefault(key, []).append(x)
        sub = [{"type": "section", "heading": k, "blocks": [{"type": "items", "items": v}]} for k, v in groups.items()]
        blocks.append({"type": "section", "heading": "Outline", "blocks": sub})
        blocks += D["tables"]
        return {"title": D["title"], "blocks": blocks}
    for lab, pairs in D["fields"]:
        blocks.append({"type": "fields", "label": lab, "pairs": pairs})
    if D["sents"]:
        if container == "form":
            for s in D["sents"]:
                blocks.append({"type": "para", "text": s})
        elif samp == "S4" and container in ("prose", "memo", "email_thread"):
            k = 3
            for i in range(0, len(D["sents"]), k):
                blocks.append({"type": "para", "text": " ".join(D["sents"][i:i + k])})
        else:
            blocks.append({"type": "items", "items": D["sents"]})
    blocks += D["tables"]
    return {"title": D["title"], "blocks": blocks}


def case_table(card: dict, S: dict) -> dict:
    ents = S["ents"]
    cur = card["cur"]
    e0 = ents[0]
    cols = ["Reference"]
    rows = []
    if "pts" in e0:
        bl = list(e0["pts"]["b"])
        cl = list(e0["pts"]["c"])
        al = list(e0["pts"]["a"])
        cols += bl + cl + al
        for e in ents:
            r = [e["id"]]
            for f in bl:
                v = e["pts"]["b"][f]
                r.append("not recorded" if v is None else ("yes" if v else "no"))
            r += [e["pts"]["c"][c] for c in cl]
            r += [money_text(e["pts"]["a"][a], cur) if e["pts"]["a"][a] is not None else "not recorded" for a in al]
            rows.append(r)
    elif e0.get("ch") is not None:
        cols += ["Event", "Chance"] + (["Loss"] if e0["ch"].get("amt") is not None else [])
        for e in ents:
            ch = e["ch"]
            r = [e["id"], ch["ev"], "not recorded" if ch["p"] is None else chance_text(ch["p"], ch["rep"], ch["den"])]
            if ch.get("amt") is not None:
                r.append(money_text(ch["amt"], cur))
            rows.append(r)
    elif e0.get("outs"):
        cols += ["Event", "Chance", "Loss"] + (["Own cost"] if e0.get("cost") is not None else [])
        for e in ents:
            o = e["outs"][0]
            r = [e["id"], o["ev"], "not recorded" if o["p"] is None else chance_text(o["p"], o["prep"], o["pden"]),
                 money_text(o["a"], cur)]
            if e.get("cost") is not None:
                r.append(e.get("cost_word") if e.get("cost_word") == "None" else money_text(e["cost"], cur))
            rows.append(r)
    return {"type": "table", "caption": None, "columns": cols, "rows": rows}


# ------------------------------------------------------------------------------------------------ question/options
def question_text(card: dict, S: dict, row: dict) -> str:
    f = S["form"]
    qv = row.get("qvar", 0)
    ents = S["ents"]
    if f == "yn_thr":
        th = S["thr"]
        neg = th["neg"]
        key = {0: "yn_thr", 1: "yn_thr_neg", 2: "yn_thr_dneg"}[neg]
        ID = ents[S["case"]]["id"]
        q = S["q"]
        if q["k"] == "post":
            qn = "chance"
            qof = f"that {ID} is classed '{card['hyp_display'][q['h']]}'"
        elif q["k"] == "risk":
            qn, qof = "risk", f"of {ID}"
        elif q["k"] in ("tec",):
            qn, qof = "total expected cost", f"for {ID}"
        else:
            qn, qof = qname(card, q), (f"of {ID}" if q["k"] == "score" else f"for {ID}")
        T = th["T"]
        tr = th.get("trep") or {}
        qt = row["qt"]
        if qt == "chance":
            Tt = chance_text(T, tr["rep"], tr.get("denom"))
        elif qt == "money":
            Tt = money_text(T, card["cur"])
        elif qt == "score":
            Tt = str(T.numerator)
        else:
            Tt = num_text(T)
        return L.QUESTIONS[key][0].format(qname=qn, qof=qof, cmp=S["cmp_word"], T=Tt)
    if f == "yn_act":
        key = {0: "yn_act", 1: "yn_act_neg", 2: "yn_act_dneg"}[S["act"]["neg"]]
        return L.QUESTIONS[key][0].format(ID=ents[S["case"]]["id"], action=S["act"]["action"])
    if f == "bin":
        return L.QUESTIONS["bin"][qv % 2].format(ID=ents[S["case"]]["id"], H=card["hyp_display"][S["q"]["h"]])
    if f == "tier":
        return L.QUESTIONS["tier"][qv % 2].format(ID=ents[S["case"]]["id"])
    if f == "mat":
        return L.QUESTIONS["mat"][qv % 2].format(ID=ents[S["case"]]["id"])
    if f == "rank_top":
        return L.QUESTIONS["rank_top"][0].format(item=card["case"]["noun"],
                                                 hl="highest" if S["hl"] == "high" else "lowest",
                                                 qname=qname(card, card["q"]))
    if f == "rank_order":
        return L.QUESTIONS["rank_order"][0].format(qname=qname(card, card["q"]))
    if f == "dec":
        return L.QUESTIONS["dec"][0].format(ID=S["dec_case"])
    if f == "pred":
        return L.QUESTIONS["pred"][qv % 2].format(ID=ents[S["case"]]["id"])
    if f == "inv":
        return L.QUESTIONS["inv"][qv % 2].format(cases=card["case"]["plural"], case=card["case"]["noun"])
    raise ValueError(f)


def order_text(S: dict, order: tuple) -> str:
    return ", ".join(S["ents"][i]["id"] for i in order)


def options_for(card: dict, S: dict) -> list:
    """Canonical option texts (before the row's display shuffle) and their answer keys: [(text, key)]."""
    f = S["form"]
    if f == "bin":
        e = card["rules"]["bins"]
        out = [(bin_range(e, card["rules"]["bin_conv"], i), i) for i in range(len(e) + 1)]
        if S["world"] == "open":
            out.append((L.CBD, "CBD"))
        return out
    if f == "tier":
        return [(t, i) for i, t in enumerate(card["rules"]["tiers"])]
    if f == "mat":
        return [(t, i) for i, t in enumerate(card["rules"]["mat"]["ratings"])]
    if f == "pred":
        return [(h, i) for i, h in enumerate(card["hyp_display"])]
    if f in ("rank_top", "inv"):
        out = [(e["id"], i) for i, e in enumerate(S["ents"])]
        if f == "inv":
            out.append((L.CBD, "CBD") if S["world"] == "open" else (L.NOTA, "NOTA"))
        elif S["world"] == "open":
            out.append((L.CBD, "CBD"))
        return out
    if f == "dec":
        out = [(e["action"], i) for i, e in enumerate(S["ents"])]
        if S["world"] == "open":
            out.append((L.CBD, "CBD"))
        return out
    if f == "rank_order":
        import itertools as it
        n = len(S["ents"])
        perms = list(it.permutations(range(n)))
        if n == 5:
            sub = S["subset"]
            perms = [p for p in perms if p.index(sub["X"]) in sub["pos"]]
        out = [(order_text(S, p), p) for p in perms]
        if n == 5:
            out.append((L.NOTA, "NOTA"))
        return out
    raise ValueError(f)


def gold_key(S: dict, ans):
    if S["form"] == "rank_order" and len(S["ents"]) == 5:
        sub = S["subset"]
        if ans.index(sub["X"]) not in sub["pos"]:
            return "NOTA"
    return ans


# ------------------------------------------------------------------------------------------------ row fields
def render_fields(card: dict, S: dict, row: dict) -> dict:
    """Raw row fields via fmt1. row: version, style, wording text, qvar, order (option display order), inert..."""
    st = fpool.style(row["style"])
    ir = card_ir(card, row["version"], row.get("examples"))
    doc = doc_ir(card, S, row, st["container"], st["skin"], row.get("people") or [])
    q = question_text(card, S, row)
    if S["form"] in ("yn_thr", "yn_act"):
        f = fcard.render_row_text(st, doc=doc, question=q, qtype="noul", card=ir, wording=row["wording"])
        return {"qtype": "noul", "options": None, **f, "_ir": ir, "_q": q}
    opts = row["options"]
    defs = option_defs(card, opts)
    ir2 = ir if ir is not None else ({"title": None, "blocks": []} if defs else None)
    if defs:
        ir2 = {"title": None, "blocks": list((ir or {}).get("blocks", [])) +
               [{"type": "defs", "variant": "DV01", "heading": None, "entries": defs}]}
    f = fcard.render_row_text(st, doc=doc, question=q, qtype="choice", card=ir2, options=opts,
                              wording=row["wording"])
    return {"qtype": "choice", "options": opts, **f, "_ir": ir2, "_q": q}
