"""F3 renderer: hidden structure + query -> row text through fmt1 (render_row_text / loader_check).

State Doc IR per card encoding: "sent" (entry sentences), "rec" / "table" (records; blanks as empty cells or
left-out keys), "notice" (S4 notices), "git" (S5 lines). Card IR from the statement registry, with masked / swapped
definitions placed by the A16.1 (g) row layout (render_row_text moves every non-definition block into instructions on
choice rows). Illustrations and worked examples are drawn on separate mini-structures and checked by solver A.
"""
from __future__ import annotations

import copy
import random
import sys

import registry as R
import solver_a as A
import textforms as TF
from cards import fill, short_card_rules, stated_rules, wording_text
from f3common import FMT1_DIR, unit_hash

sys.path.insert(0, str(FMT1_DIR))
from fmt1 import card as fmt1_card  # noqa: E402
from fmt1 import pool as fmt1_pool  # noqa: E402
from fmt1.render import BLANK, OMIT, FormatError  # noqa: E402


def by_number(S):
    return {e["n"]: e for e in S["entries"]}


# ------------------------------------------------------------------------------------------------ state

def _title(c):
    return f"{c['org']}: {c['item_pl']} log"


def _with_gaps_sent(c, S, lines_by_n):
    """Entry lines with explicit gap markers after the entries named in S['gaps']."""
    out = []
    for e in _listed(c, S):
        out.append(lines_by_n[e["n"]])
        if S.get("gap_style") == "explicit" and e["n"] in S.get("gaps", []):
            out.append(c["gap_marker"])
    return out


def _listed(c, S):
    """Entries in listing order (chronological, sorted by a stated key, shuffled with timestamps, S6 orders)."""
    ents = list(S["entries"])
    lo = S.get("list_order")
    if lo:
        pos = {n: i for i, n in enumerate(lo)}
        return sorted(ents, key=lambda e: pos[e["n"]])
    return ents


def set_listing(c, S, rng):
    """Fix S['list_order'] (entry numbers in display order) from the card's listing toggle."""
    ents = list(S["entries"])
    lst = c["listing"]
    if lst == "sorted":
        def key(e):
            subj = e.get("item") or e.get("old") or e.get("absorbed") or e.get("record") or ""
            return (subj == "", subj, e["n"])
        order = sorted(ents, key=key)
    elif lst == "shuffled":
        order = ents[:]
        rng.shuffle(order)
    elif lst == "eff_sorted":
        order = sorted(ents, key=lambda e: ((e.get("eff") or e["date"]), e["n"]))
    elif lst == "newest_first":
        order = ents[::-1]
    else:
        order = ents
    S["list_order"] = [e["n"] for e in order]


def doc_sent(c, S, notes, container):
    by_n = by_number(S)
    lines = {e["n"]: TF.entry_sentence(c, S, e, by_n, note=notes.get(e["n"])) for e in S["entries"]}
    blocks = []
    reg = TF.register_lines(c, S)
    if S["sampler"] == "S6":
        head = R.SNAPSHOT_HEAD[0].format(d0=TF.dt_text(c, S["d0"]))
    else:
        head = R.REGISTER_HEAD[c["reg_v"]]
    if container == "log_lines":
        ev = []
        for e in _listed(c, S):
            ts, tx = TF.entry_log_line(c, S, e, by_n, note=notes.get(e["n"]))
            ev.append({"ts": ts, "text": tx})
        return {"title": _title(c), "blocks": [{"type": "events", "events": ev}]}
    if reg:
        blocks.append({"type": "section", "heading": head, "blocks": [{"type": "items", "items": reg}]})
    blocks.append({"type": "section", "heading": R.LOG_HEAD[c["reg_v"]],
                   "blocks": [{"type": "items", "items": _with_gaps_sent(c, S, lines)}]})
    return {"title": _title(c), "blocks": blocks}


def doc_records(c, S, notes, container, blank):
    by_n = by_number(S)
    cols = TF.record_columns(c, S)
    rows = []
    for e in _listed(c, S):
        r = TF.record_row(c, S, e, by_n, note=notes.get(e["n"]))
        rows.append([r.get(col, blank) for col in cols])
    blocks = []
    if S["register"]["items"]:
        rc = TF.register_columns(c, S)
        rr = []
        for item, holder, status, qty in S["register"]["items"]:
            row = [item, holder, status] + ([qty] if S["has_qty"] else [])
            rr.append(row)
        head = (R.SNAPSHOT_HEAD[0].format(d0=TF.dt_text(c, S["d0"])) if S["sampler"] == "S6"
                else R.REGISTER_HEAD[c["reg_v"]])
        blocks.append({"type": "table", "caption": head, "columns": rc, "rows": rr})
    if S["register"].get("docs"):
        blocks.append({"type": "table", "caption": "Documents", "columns": [R.REG_COL["doc"], R.REG_COL["rec"]],
                       "rows": [[d, r] for d, r in S["register"]["docs"]]})
    split = len(rows) >= 8 and unit_hash("split", c["card_id"], S.get("_log_id", "")) < 0.4
    if split:
        a = [r for r, e in zip(rows, _listed(c, S)) if e["t"] in ("CREATE", "SET", "ADJUST", "TRANSFER")]
        b = [r for r, e in zip(rows, _listed(c, S)) if e["t"] not in ("CREATE", "SET", "ADJUST", "TRANSFER")]
        if a and b:
            blocks.append({"type": "table", "caption": "Item changes", "columns": cols, "rows": a})
            blocks.append({"type": "table", "caption": "Other changes", "columns": cols, "rows": b})
        else:
            split = False
    if not split:
        blocks.append({"type": "table", "caption": R.LOG_HEAD[c["reg_v"]], "columns": cols, "rows": rows})
    return {"title": _title(c), "blocks": blocks}


def doc_notices(c, S, notes, container, skin):
    by_n = by_number(S)
    nts = TF.notice_texts(c, S, by_n, notes)
    reg = TF.register_lines(c, S)
    if container in ("email_thread", "chat_log"):
        msgs = []
        if reg:
            msgs.append({"speaker": "Registry desk", "text": "\n".join([R.REGISTER_HEAD[c["reg_v"]] + "."] + reg)
                         if container == "email_thread" else " ".join([R.REGISTER_HEAD[c["reg_v"]] + "."] + reg)})
        for ref, d, frm, to, lines in nts:
            if container == "email_thread":
                msgs.append({"speaker": frm, "to": to, "ts": TF.dt_text(c, d), "subject": f"Notice {ref}",
                             "text": "\n".join(lines)})
            else:
                msgs.append({"speaker": frm, "text": " ".join(lines)})
            if S.get("gap_style") == "explicit" and ref in S.get("gap_after_refs", []):
                raise FormatError("explicit markers are not shown in threads")
        if container == "email_thread" and reg:
            msgs[0].update({"to": msgs[1]["to"] if len(msgs) > 1 else "all", "ts": TF.dt_text(c, nts[0][1]),
                            "subject": "Register"})
        return {"title": _title(c) if container == "email_thread" else None,
                "blocks": [{"type": "messages", "messages": msgs}]}
    blocks = []
    if reg:
        blocks.append({"type": "section", "heading": R.REGISTER_HEAD[c["reg_v"]],
                       "blocks": [{"type": "items", "items": reg}]})
    for ref, d, frm, to, lines in nts:
        blocks.append({"type": "section", "heading": f"From {frm} to {to}", "blocks": [{"type": "items", "items": lines}]})
        if S.get("gap_style") == "explicit" and ref in S.get("gap_after_refs", []):
            blocks.append({"type": "para", "text": c["gap_marker"]})
    return {"title": _title(c), "blocks": blocks}


def doc_git(c, S, container):
    by_n = by_number(S)
    hashes = {int(k): v for k, v in (S.get("hashes") or {}).items()}
    for e in S["entries"]:
        if e["n"] not in hashes:
            import hashlib
            hashes[e["n"]] = hashlib.sha256(f"{S.get('_log_id')}:{e['n']}".encode()).hexdigest()[:12]
    lines = [TF.git_line(c, S, e, by_n, hashes) for e in _listed(c, S)]
    if container == "log_lines":
        ev = []
        for e, ln in zip(_listed(c, S), lines):
            dt = TF.dt_text(c, e["date"], e.get("time"))
            ev.append({"ts": dt, "text": ln.replace(" " + dt + " ", " ", 1)})
        return {"title": _title(c), "blocks": [{"type": "events", "events": ev}]}
    return {"title": _title(c), "blocks": [{"type": "items", "items": lines}]}


def build_doc(c, S, notes, style):
    cont = style["container"]
    enc = c["encoding"]
    if enc == "sent":
        return doc_sent(c, S, notes, cont)
    if enc in ("rec", "table"):
        blank = OMIT if cont in ("json", "yaml", "key_value") else BLANK
        return doc_records(c, S, notes, cont, blank)
    if enc == "notice":
        return doc_notices(c, S, notes, cont, style["skin"])
    if enc == "git":
        return doc_git(c, S, cont)
    raise ValueError(enc)


# ------------------------------------------------------------------------------------------------ card IR

def rule_sentence(c, tid, extra):
    v = c["t_v"].get(tid, 0) % len(R.T[tid])
    return fill(R.T[tid][v], c, extra)


def card_ir(c, S, *, qtype, options, illus=None, fewshot=None, row_rng=None):
    """The card IR for one row; None on no-card rows."""
    if c["def_style"] == "none":
        return None
    extra = {"N0": str(S.get("n0") or ""), "D0": TF.dt_text(c, S["d0"]) if S.get("d0") else "",
             "Dlast": TF.dt_text(c, max(e["date"] for e in S["entries"])) if S["entries"] else "",
             "listing": "newest first" if c["listing"] == "newest_first" else "oldest first"}
    if c["def_style"] == "short":
        rules, _dropped = short_card_rules(c)
    else:
        rules = stated_rules(c)
    task = fill(R.TASK_LINES[c["task_v"]], c)
    blocks = [{"type": "task", "text": task}]
    sents, names = [], []
    vocab_blocks = []
    for t in rules:
        if t in ("T36m", "T36s"):
            continue
        if t == "T35":
            continue
        sents.append(rule_sentence(c, t, extra))
        names.append(R.T_NAMES[t])
    # vocabulary definitions (masked / swapped): option-definition entries for shown status options on choice rows
    if c["vocab"] in ("masked", "swapped"):
        shown = set(options or []) if qtype == "choice" else set()
        ents, rest = [], []
        for code in c["statuses"]:
            meaning = c["status_meaning"][code]
            if code in shown:
                ents.append({"name": code, "text": meaning})
            else:
                key = "T36m" if c["vocab"] == "masked" else "T36s"
                txt = R.T[key][c["t_v"].get(key, 0) % len(R.T[key])]
                rest.append(fill(txt, c, {"code": code, "word": code, "meaning": meaning}))
        if ents:
            vocab_blocks.append({"type": "defs", "variant": "DV01", "entries": ents})
        if rest:
            vocab_blocks.append({"type": "items", "items": rest})
    st = c["def_style"]
    if st in ("one_line", "one_line_examples", "short"):
        blocks.append({"type": "items", "items": sents})
    elif st == "decision_list":
        blocks.append({"type": "items", "items": sents})
        t35 = rule_sentence(c, "T35", extra)
        blocks.append({"type": "steps", "items": [t35]})
    elif st == "rubric_table":
        blocks.append({"type": "table", "columns": ["Rule", "Meaning"],
                       "rows": [[n, s_] for n, s_ in zip(names, sents)], "caption": None})
    blocks += vocab_blocks
    if illus and st == "one_line_examples":
        for txt in illus:
            blocks.append({"type": "para", "text": txt})
    if fewshot:
        blocks.append({"type": "fewshot", "template": fewshot["template"], "heading": None,
                       "examples": fewshot["examples"]})
    return {"title": None, "blocks": blocks}


# ------------------------------------------------------------------------------------------------ mini-structures

def mini_structure(c, rng, kind):
    """A 2-4 entry structure on EX-prefixed IDs for an illustration or worked example. Returns (S, Q) or None."""
    S = {"sampler": "S1" if c["sampler"] not in ("S4", "S6", "S5") else "S1", "world": "closed", "gap_style": None,
         "n0": None, "toggles": {"rename_mode": c["rename_mode"], "check": c["check"], "lock": c["lock"],
                                 "lock_status": c["lock_status"], "timed": False},
         "has_qty": False, "statuses": list(c["statuses"]), "default_status": c["default_status"],
         "register": {"items": [], "docs": []}, "entries": [], "gaps": []}
    st = c["statuses"]
    y = "EX-" + rng.choice("KMPQRTVW") + str(rng.randint(2, 9)) + rng.choice("HJNX") + str(rng.randint(2, 9))
    h1, h2, h3 = (f"XH-{rng.randint(201, 299)}" for _ in range(3))
    if len({h1, h2, h3}) < 3:
        return None
    d = ["2030-01-0%d" % i for i in range(2, 9)]
    E = []

    def add(e):
        e["n"] = len(E) + 1
        e["date"] = d[len(E)]
        e["time"] = None
        E.append(e)
    s1, s2, s3 = rng.sample(st, 3) if len(st) >= 3 else (st[0], st[1], st[0])
    add({"t": "CREATE", "item": y, "holder": h1, "status": s1, "qty": None})
    Q = None
    if kind == "VOID":
        add({"t": "SET", "item": y, "field": "status", "value": s2})
        add({"t": "VOID", "target": 2})
        Q = {"qt": "Q1", "form": "yn", "kind": "status", "item": y, "value": s1, "point": {"kind": "end"}}
    elif kind == "CORR":
        add({"t": "SET", "item": y, "field": "status", "value": s2})
        add({"t": "CORR", "target": 2, "slot": "value", "value": s3})
        Q = {"qt": "Q1", "form": "yn", "kind": "status", "item": y, "value": s3, "point": {"kind": "end"}}
    elif kind == "SUPERSEDE":
        S["register"]["docs"] = [["EXD-11", "EXR-K4M2"]]
        E.pop()
        add({"t": "SUPERSEDE", "old": "EXR-K4M2", "new": "EXR-P7W3"})
        add({"t": "SUPERSEDE", "old": "EXR-P7W3", "new": "EXR-T9H5"})
        add({"t": "VOID", "target": 2})
        Q = {"qt": "Q3", "form": "yn", "kind": "record", "doc": "EXD-11", "record": "EXR-P7W3"}
    elif kind == "RENAME" and c["rename_mode"]:
        add({"t": "RENAME", "kind": "holder", "old": h1, "new": h2})
        add({"t": "TRANSFER", "item": y, "sender": h1, "receiver": h3})
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": h3, "point": {"kind": "end"}}
    elif kind == "MERGE":
        add({"t": "MERGE", "absorbed": h1, "survivor": h2})
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": h2, "point": {"kind": "end"}}
    elif kind == "CHECK" and c["check"]:
        add({"t": "TRANSFER", "item": y, "sender": h2, "receiver": h3})
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": h3, "point": {"kind": "end"}}
    elif kind == "CHECK" and c["lock"]:
        add({"t": "SET", "item": y, "field": "status", "value": c["lock_status"]})
        add({"t": "TRANSFER", "item": y, "sender": h1, "receiver": h3})
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": h3, "point": {"kind": "end"}}
    else:
        add({"t": "TRANSFER", "item": y, "sender": h1, "receiver": h2})
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": h2, "point": {"kind": "end"}}
    S["entries"] = E
    if A.check_rules(S):
        return None
    Q.update(neg="A", end_word="at the end")
    return S, Q


def _mini_card(c):
    m = dict(c)
    m["timed"] = False
    m["_doctype"] = {"EXD-11": "document"}
    return m


def mini_text(c, S):
    mc = _mini_card(c)
    by_n = by_number(S)
    parts = []
    for doc, rec in S["register"].get("docs", []):
        parts.append(R.REGISTER_DOC[0].format(doctype="document", doc=doc, rec=rec))
    for e in S["entries"]:
        parts.append(R.HEADER_LOG.format(n=e["n"]) + TF.body_text(mc, S, e, variant=0, by_n=by_n))
    return " ".join(parts)


def illustrations(c, rng):
    """1-2 illustrations of the riskiest rules (one_line_examples cards). Each: entries + a result claim."""
    pref = [m for m in ("VOID", "CORR", "SUPERSEDE", "RENAME", "MERGE", "CHECK") if m in c["mechs"]] or ["PLAIN"]
    out = []
    for kind in pref[:c.get("n_illus", 1)]:
        got = mini_structure(c, rng, kind)
        if not got:
            continue
        S, Q = got
        lab = A.answer(S, Q)
        claim = _claim_text(c, S, Q, positive=bool(lab))
        pre = R.ILLUS_PREFIX[c["t_v"].get("T1", 0) % 2]
        res = R.ILLUS_RESULT[c["t_v"].get("T1", 0) % 2]
        out.append(pre + mini_text(c, S) + " " + res + claim + ".")
    return out


def _claim_text(c, S, Q, positive=True):
    mc = _mini_card(c)
    q = dict(Q, neg="A" if positive else "N1", kinds=False, end_word="at the end")
    key = {"Q1": ("status", "end"), "Q3": ("record", "end"), "Q4": ("holder", "end")}[Q["qt"]]
    st = R.STEM[key]
    v = {"field": c["field"], "Y": Q.get("item", ""), "X": Q.get("holder", ""), "S": Q.get("value", ""),
         "END": "at the end", "R": Q.get("record", ""), "DOC": Q.get("doc", ""), "doctype": "document"}
    return (st["C"] if positive else st["Cn"]).format(**v)


def fewshot_block(c, rng):
    tmpl = rng.choice(["FT01", "FT03", "FT05", "FT11", "FT12", "FT14"])
    exs = []
    kinds = [m for m in ("VOID", "CORR", "SUPERSEDE", "MERGE", "CHECK") if m in c["mechs"]] + ["PLAIN"]
    for kind in kinds[:rng.randint(1, 3)]:
        got = mini_structure(c, rng, kind)
        if not got:
            continue
        S, Q = got
        if rng.random() < 0.5 and Q["qt"] in ("Q1", "Q4"):
            Q = dict(Q)
            if Q["qt"] == "Q1":
                Q["value"] = [s for s in c["statuses"] if s != Q["value"]][0]
            else:
                Q["holder"] = "XH-300"
        lab = A.answer(S, Q)
        if lab not in (0, 1):
            continue
        q = TF.stem_text(_mini_card(c), S, dict(Q, kinds=False))
        exs.append({"case": mini_text(c, S) + "\nQuestion: " + q, "answer": "Yes" if lab == 1 else "No"})
    if not exs:
        return None
    return {"template": tmpl, "examples": exs}


# ------------------------------------------------------------------------------------------------ row text

def pick_style(c, key, tries=0):
    sts = c["styles"]
    i = int(unit_hash("style", c["card_id"], key, tries) * len(sts))
    return fmt1_pool.style(sts[i])


def pick_wording(c, form, key):
    ws = [w for w in c["wordings"] if _wforms(w) in (("any",), ("yn",) if form == "yn" else ("choice",))]
    return ws[int(unit_hash("wording", c["card_id"], key) * len(ws))]


def yn_wordings(c):
    """The card's wordings a yes/no row may take (same filter as pick_wording)."""
    return [w for w in c["wordings"] if _wforms(w) in (("any",), ("yn",))]


def _wforms(wid):
    from cards import WORDINGS
    return tuple(WORDINGS[wid]["forms"])


class LengthError(ValueError):
    """No style of the card renders this row under the token cap."""


def render_row(c, S, spec, notes, *, row_key, illus=None, fewshot=None, measure=None, cap=1900, style_ids=None,
               wid=None):
    """Row text fields + loader check for one row spec, in the first style of the card's set (hash order) that
    renders, passes fmt1 loader_check and, when `measure` is given, stays under `cap` real tokens on the served
    prompt. Returns (fields, check, style, wording_id, card_ir, question, tokens)."""
    Q = spec["Q"]
    qtype = "choice" if Q["form"] == "choice" else "noul"
    question = TF.stem_text(c, S, Q)
    wid = wid or pick_wording(c, Q["form"], row_key)
    wtext = wording_text(wid, c.get("locale", "US"))
    opts = spec.get("options") if qtype == "choice" else None
    last = None
    best_len = None
    pool_ids = list(style_ids) if style_ids else list(c["styles"])
    n = len(pool_ids)
    start = int(unit_hash("style", c["card_id"], row_key) * n)
    for j in range(n):
        st = fmt1_pool.style(pool_ids[(start + j) % n])
        try:
            doc = build_doc(c, S, notes, st)
            cir = card_ir(c, S, qtype=qtype, options=opts, illus=illus, fewshot=fewshot)
            fields = fmt1_card.render_row_text(st, doc=doc, question=question, qtype=qtype, card=cir,
                                               options=opts, wording=wtext)
            gold = spec["gold"] if qtype == "choice" else int(spec["gold"])
            row = {"id": row_key, "qtype": qtype, "options": list(opts) if opts else None, "gold": gold, **fields}
            res = fmt1_card.loader_check(row, must_show=fmt1_card.must_show(cir, question=question, wording=wtext),
                                         seed="f3-loader")
            if not res["ok"]:
                last = ("loader", res["problems"][:3])
                continue
            tok = measure(row) if measure else None
            if tok is not None and tok >= cap:
                best_len = tok if best_len is None else min(best_len, tok)
                last = ("length", tok)
                continue
            return fields, res, st, wid, cir, question, tok
        except FormatError as ex:
            last = ("format", str(ex)[:120])
            continue
    if last and last[0] == "length":
        raise LengthError(f"shortest style {best_len} tokens")
    raise FormatError(f"no style rendered the row: {last}")
