"""F6 renderer: structure -> fmt1 card IR + Doc IR + question + options, then fmt1 card.render_and_check.

Where each part goes (G0 1.1, A16.1 (g)): switch sentences, policy, glosses and examples are card IR blocks; the
record (case data only) is the Doc IR; options are option text only. fmt1 moves every card block except option
definition lines into `instructions` on choice rows. The parser (parse_f6.py) never imports this module.
"""
from __future__ import annotations

from .common import iso, month_name_date, ymd, MONTHS, days_in_month
from .lex import sw, join_or, join_and, FRAMES

CMP_WORDS = {">=": ["at least", "no fewer than", "no less than"], "<=": ["at most", "no more than"],
             ">": ["more than", "above", "exceeds"], "<": ["fewer than", "less than", "below"]}


def a_or_an(w: str) -> str:
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def fmt_date(d: int, style: str) -> str:
    return iso(d) if style == "iso" else month_name_date(d)


def date_phrase(dd: dict, style: str) -> str:
    """Exact, ranged ('from a to b') or month-only ('in March 2047 (31 days)') date phrase."""
    if dd["k"] == "exact":
        return fmt_date(dd["d"], style)
    if dd["k"] == "range":
        return f"from {fmt_date(dd['a'], style)} to {fmt_date(dd['b'], style)}"
    y, m = dd["y"], dd["m"]
    return f"in {MONTHS[m - 1]} {y} ({days_in_month(y, m)} days)"


# ---------------------------------------------------------------- atoms and rules (rules kind)

def atom_text(R: dict, at: dict, names: dict) -> str:
    cn = R["case_noun"]
    t = at["t"]
    if t == "num":
        a = R["attrs"][at["a"]]
        w = names["cmp"][at["op"]]
        if w == "exceeds":
            return f"the {a['name']} exceeds {at['n']} {a['unit']}"
        return f"the {a['name']} is {w} {at['n']} {a['unit']}"
    if t == "cat":
        a = R["attrs"][at["a"]]
        return f"the {a['name']} is {at['v']}"
    if t == "ev":
        e = R["events"][at["e"]]["name"]
        if at.get("neg"):
            return f'the {cn} did not have {a_or_an(chr(34) + e + chr(34))} event'
        return f'the {cn} had {a_or_an(chr(34) + e + chr(34))} event'
    if t == "cls":
        return f"the {cn} is {a_or_an(R['classes'][at['c']]['name'])}"
    raise ValueError(t)


def outname(R: dict, oid: str, nm: dict) -> str:
    return nm["out"][oid]


def rule_text(R: dict, r: dict, nm: dict) -> str:
    conds = " and ".join(atom_text(R, a, nm) for a in r["conds"])
    s = f'In {R["notices"][r["notice"]]["name"]}, the outcome is "{outname(R, r["out"], nm)}" if {conds}'
    if r.get("unless"):
        s += f", unless {atom_text(R, r['unless'], nm)}"
    return s + "."


def notice_text(R: dict, nid: str, style: str) -> str:
    n = R["notices"][nid]
    d = n["date"]
    if d["k"] == "exact":
        return f"{cap(n['name'])} takes effect on {fmt_date(d['d'], style)}."
    return f"{cap(n['name'])} takes effect on one day {date_phrase(d, style)}." if d["k"] == "range" else \
        f"{cap(n['name'])} takes effect on one day {date_phrase(d, style)}."


def policy_blocks(R: dict, nm: dict, defs_style: str, style_date: str, heading: str, dl_variant: str | None):
    """Card IR blocks for the policy: notices, numbered rules (items 'Rule k: ...' or a decision list), exceptions,
    only-if statements, subclass relations and the outcome table. Returns (blocks, rule_number_of_rid)."""
    items_pre = [notice_text(R, nid, style_date) for nid in R["notice_order"]]
    num = {}
    rules_txt = []
    k = 0
    for r in R["rules"]:
        if r.get("exc"):
            continue
        k += 1
        num[r["rid"]] = k
        rules_txt.append(rule_text(R, r, nm))
    T = R.get("table")
    if T:
        k += 1
        num[T["rid"]] = k
    exc_txt = []
    for r in R["rules"]:
        if not r.get("exc"):
            continue
        tgt = r["exc"]
        if T and tgt.startswith(T["rid"] + ":"):
            a, b = tgt.split(":", 1)[1].split("|", 1)
            head = f"Exception to rule {num[T['rid']]}, cell {a} / {b}"
        else:
            head = f"Exception to rule {num[tgt]}"
        exc_txt.append(f"{head}: {rule_text(R, r, nm)}")
    oi_txt = [f'The outcome is "{nm["out"][o["out"]]}" only if {atom_text(R, o["cond"], nm)}.'
              for o in R.get("onlyif", [])]
    sub_txt = [f"Every {R['classes'][b]['name']} is {a_or_an(R['classes'][a]['name'])}."
               for b, a in R.get("subclass", [])]
    blocks = []
    pol = list(items_pre)
    if dl_variant:
        blocks.append({"type": "items", "items": pol})
        blocks.append({"type": "defs", "variant": dl_variant, "heading": None,
                       "entries": [{"name": None, "text": t} for t in rules_txt]} if dl_variant != "DV35" else
                      {"type": "defs", "variant": dl_variant, "heading": None,
                       "entries": [{"name": f"Rule {i + 1}", "text": t} for i, t in enumerate(rules_txt)]})
        rest = exc_txt + oi_txt + sub_txt
    else:
        pol += [f"Rule {i + 1}: {t}" for i, t in enumerate(rules_txt)]
        rest = exc_txt + oi_txt + sub_txt
        blocks.append({"type": "items", "items": pol})
    if T:
        A, B = R["attrs"][T["A"]]["name"], R["attrs"][T["B"]]["name"]
        lead = (f"Rule {num[T['rid']]}: In {R['notices'][T['notice']]['name']}, the outcome table below gives the "
                f"outcome by the {A} (rows) and the {B} (columns).")
        rows = [[a] + [nm["out"][T["cells"][f"{a}|{b}"]] for b in T["cols"]] for a in T["rows"]]
        blocks.append({"type": "items", "items": [lead]})
        blocks.append({"type": "table", "columns": [cap(A)] + list(T["cols"]), "rows": rows, "caption": None})
    if rest:
        blocks.append({"type": "items", "items": rest})
    return [{"type": "section", "heading": heading, "blocks": blocks}], num


def unit_values(R):
    return R


# ---------------------------------------------------------------- record (Doc IR) for the rules kind

def fact_value(R: dict, kind: str, key: str, f: dict, case: str, style_date: str) -> str:
    mk = R["marker"]
    tag = (R.get("ev_tag") or {}).get("tag")
    if f.get("m"):
        return mk
    if kind == "num":
        s = f"{f['v']} {R['attrs'][key]['unit']}"
    elif kind == "cat":
        s = str(f["v"])
    elif kind == "ev":
        s = fmt_date(f["date"], style_date)
    else:
        raise ValueError(kind)
    if f.get("tag"):
        s += f" ({tag})"
    return s


def record_doc(R: dict, case_list: list, style_date: str, title: str | None) -> dict:
    """One fields block per case (a section per case on C-CASE rows)."""
    blocks = []
    multi = len(case_list) > 1
    for case in case_list:
        F = R["facts"][case]
        pairs = []
        if not multi:
            pairs.append(["As-of date", fmt_date(R["D"], style_date)])
        for aid in R["attr_order"]:
            a = R["attrs"][aid]
            f = F["num" if a["kind"] == "num" else "cat"].get(aid)
            if f is not None:
                pairs.append([cap(a["name"]), fact_value(R, a["kind"], aid, f, case, style_date)])
        for eid in R["event_order"]:
            f = F["ev"].get(eid)
            if f is not None:
                pairs.append([f"{cap(R['events'][eid]['name'])} for {case}",
                              fact_value(R, "ev", eid, f, case, style_date)])
        if not multi:
            pairs += list_pairs(R)
        for k, v in F.get("inert", []):
            pairs.append([k, v])
        blk = {"type": "fields", "pairs": pairs}
        if multi:
            blocks.append({"type": "section", "heading": case, "blocks": [blk]})
        else:
            blocks.append(blk)
    if multi:
        blocks.insert(0, {"type": "fields", "pairs": [["As-of date", fmt_date(R["D"], style_date)]]})
        lp = list_pairs(R)
        if lp:
            blocks.append({"type": "fields", "pairs": lp})
    doc = {"blocks": blocks}
    if title:
        doc["title"] = title
    return doc


def join_or_vals(vals: list) -> str:
    vals = [str(v) for v in vals]
    if len(vals) == 1:
        return vals[0]
    if len(vals) == 2:
        return f"{vals[0]} or {vals[1]}"
    return ", ".join(vals[:-1]) + ", or " + vals[-1]


def list_pairs(R: dict) -> list:
    out = []
    for cid in R["class_order"]:
        members = R["lists"].get(cid)
        if not members:
            continue
        ents = []
        for who, st in members:
            if st == "m":
                ents.append(f"{who} (membership {R['marker']})")
            elif st == "tag":
                ents.append(f"{who} ({R['ev_tag']['tag']})")
            else:
                ents.append(who)
        out.append([cap(R["classes"][cid]["plural"]), ", ".join(ents)])
    return out
