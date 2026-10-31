"""Surface forms: entry sentences, register lines, record rows, S4 notices, S5 git lines and question stems, all
filled from the registry templates. Used by the renderer and by the card builder (illustrations, worked examples).
The parser never imports this module.
"""
from __future__ import annotations

import registry as R
from f3common import fmt_date


def dt_text(c, date, time=None):
    s = fmt_date(date, c["date_fmt"])
    if c.get("timed") and time:
        s += " " + time
    return s


def _base(c):
    return {"field": c["field"], "qty": c["qty"] or "", "unit": c["unit"] or "", "kind": c["item_sg"],
            "hnoun": c["holder_sg"]}


def body_key(e, S):
    t = e["t"]
    if t == "CREATE":
        hs, hq = e.get("status") is not None, (e.get("qty") is not None and S["has_qty"])
        return "CREATE_full" if hs and hq else "CREATE_s" if hs else "CREATE_q" if hq else "CREATE_0"
    if t == "SET":
        return "SET_status" if e["field"] == "status" else "SET_qty"
    if t == "ADJUST":
        return "ADJUST_up" if e["sign"] > 0 else "ADJUST_down"
    if t == "CORR":
        return None
    if t == "RENAME":
        return "RENAME_item" if e["kind"] == "item" else "RENAME_holder"
    return t


def corr_key(e, tgt):
    s = e["slot"]
    if s == "value":
        return "CORR_value_s" if tgt["field"] == "status" else "CORR_value_q"
    if s == "amount":
        return "CORR_amount_up" if tgt["sign"] > 0 else "CORR_amount_down"
    if s == "receiver":
        return "CORR_receiver"
    return "CORR_status" if s == "status" else "CORR_qty"


def body_text(c, S, e, variant=None, by_n=None):
    """The sentence body of one entry (no header)."""
    v = _base(c)
    t = e["t"]
    if t == "CORR":
        tgt = by_n[e["target"]]
        key = corr_key(e, tgt)
        v.update(t=_ref_of(S, tgt), s=e["value"], q=e["value"], a=e["value"], receiver=e["value"])
    else:
        key = body_key(e, S)
        v.update(item=e.get("item", ""), holder=e.get("holder", ""), sender=e.get("sender", ""),
                 receiver=e.get("receiver", ""), s=e.get("value") if t == "SET" else e.get("status", ""),
                 q=e.get("value") if t == "SET" else e.get("qty", ""), a=e.get("amount", ""),
                 t=_ref_of(S, by_n[e["target"]]) if t == "VOID" else "", rec=e.get("record", ""),
                 doc=e.get("doc", ""), doctype=c.get("_doctype", {}).get(e.get("doc"), "document"),
                 old=e.get("old") or e.get("absorbed", ""), new=e.get("new") or e.get("survivor", ""))
    tmpl = R.BODY[key]
    i = (c["body_v"].get(key, 0) if variant is None else variant) % len(tmpl)
    return tmpl[i].format(**v)


def _ref_of(S, e):
    if S["sampler"] == "S4":
        return f"{e['ref']}.{e['k']}"
    return str(e["n"])


def header_text(c, S, e):
    if S["sampler"] == "S6":
        if e["t"] in ("VOID", "CORR"):
            return R.HEADERS6V[c["header_v"]].format(n=e["n"], rd=dt_text(c, e["date"]))
        return R.HEADERS6[c["header_v"]].format(n=e["n"], rd=dt_text(c, e["date"]), ed=dt_text(c, e["eff"]))
    return R.HEADERS[c["header_v"]].format(n=e["n"], dt=dt_text(c, e["date"], e.get("time")))


def entry_sentence(c, S, e, by_n, note=None):
    s = header_text(c, S, e) + body_text(c, S, e, by_n=by_n)
    if note:
        s = s[:-1] + R.NOTE_TAIL.format(text=note) + "."
    return s


def entry_log_line(c, S, e, by_n, note=None):
    """(ts, text) for log-line containers."""
    s = R.HEADER_LOG.format(n=e["n"]) + body_text(c, S, e, by_n=by_n)
    if note:
        s = s[:-1] + R.NOTE_TAIL.format(text=note) + "."
    return dt_text(c, e["date"], e.get("time")), s


def register_lines(c, S):
    out = []
    for item, holder, status, qty in S["register"]["items"]:
        if S["has_qty"]:
            out.append(R.REGISTER_ITEM[c["reg_v"]].format(item=item, holder=holder, field=c["field"], s=status,
                                                          qty=c["qty"], q=qty, unit=c["unit"]))
        else:
            out.append(R.REGISTER_ITEM_NQ[c["reg_v"]].format(item=item, holder=holder, field=c["field"], s=status))
    for doc, rec in S["register"].get("docs", []):
        out.append(R.REGISTER_DOC[c["reg_v"]].format(doctype=c["_doctype"][doc], doc=doc, rec=rec))
    return out


# ------------------------------------------------------------------------------------------------ records

def record_columns(c, S):
    cols = [R.COL["entry"]]
    if S["sampler"] == "S6":
        cols += [R.COL["recorded"], R.COL["effective"]]
    else:
        cols.append(R.COL["date"])
        if c.get("timed"):
            cols.append(R.COL["time"])
    cols += [R.COL["subject"], R.COL["action"], c["field"][:1].upper() + c["field"][1:]]
    if S["has_qty"]:
        cols.append(f"{c['qty'][:1].upper() + c['qty'][1:]} ({c['unit']})")
    cols += [R.COL["from"], R.COL["to"], R.COL["refers"]]
    if c.get("notes_on"):
        cols.append(R.COL["note"])
    return cols


def record_row(c, S, e, by_n, note=None):
    """{column: value} for one entry (missing keys = blank)."""
    cols = record_columns(c, S)
    st_col = cols[cols.index(R.COL["action"]) + 1]
    q_col = cols[cols.index(st_col) + 1] if S["has_qty"] else None
    r = {R.COL["entry"]: e["n"]}
    if S["sampler"] == "S6":
        r[R.COL["recorded"]] = dt_text(c, e["date"])
        if e["t"] not in ("VOID", "CORR"):
            r[R.COL["effective"]] = dt_text(c, e["eff"])
    else:
        r[R.COL["date"]] = dt_text(c, e["date"])
        if c.get("timed"):
            r[R.COL["time"]] = e["time"]
    t = e["t"]
    A = R.ACTIONS
    if t == "CREATE":
        r.update({R.COL["subject"]: e["item"], R.COL["action"]: A["CREATE"], R.COL["to"]: e["holder"]})
        if e.get("status") is not None:
            r[st_col] = e["status"]
        if q_col and e.get("qty") is not None:
            r[q_col] = e["qty"]
    elif t == "SET":
        r.update({R.COL["subject"]: e["item"], R.COL["action"]: A["SET"]})
        if e["field"] == "status":
            r[st_col] = e["value"]
        else:
            r[q_col] = e["value"]
    elif t == "ADJUST":
        r.update({R.COL["subject"]: e["item"], R.COL["action"]: A["ADJUST_up" if e["sign"] > 0 else "ADJUST_down"],
                  q_col: e["amount"]})
    elif t == "TRANSFER":
        r.update({R.COL["subject"]: e["item"], R.COL["action"]: A["TRANSFER"], R.COL["from"]: e["sender"],
                  R.COL["to"]: e["receiver"]})
    elif t == "VOID":
        r.update({R.COL["action"]: A["VOID"], R.COL["refers"]: e["target"]})
    elif t == "CORR":
        tgt = by_n[e["target"]]
        s = e["slot"]
        if s == "amount":
            r[R.COL["action"]] = A["CORR_up" if tgt["sign"] > 0 else "CORR_down"]
            r[q_col] = e["value"]
        else:
            r[R.COL["action"]] = A["CORR"]
            if s == "receiver":
                r[R.COL["to"]] = e["value"]
            elif s in ("status",) or (s == "value" and tgt["field"] == "status"):
                r[st_col] = e["value"]
            else:
                r[q_col] = e["value"]
        r[R.COL["refers"]] = e["target"]
    elif t == "SUPERSEDE":
        r.update({R.COL["subject"]: e["old"], R.COL["action"]: A["SUPERSEDE"], R.COL["to"]: e["new"]})
    elif t == "OPEN":
        r.update({R.COL["subject"]: e["record"], R.COL["action"]: A["OPEN"], R.COL["to"]: e["doc"]})
    elif t == "RENAME":
        r.update({R.COL["subject"]: e["old"], R.COL["action"]: A["RENAME"], R.COL["to"]: e["new"]})
    elif t == "MERGE":
        r.update({R.COL["subject"]: e["absorbed"], R.COL["action"]: A["MERGE"], R.COL["to"]: e["survivor"]})
    if note and c.get("notes_on"):
        r[R.COL["note"]] = note
    return r


def register_columns(c, S):
    cols = [c["item_sg"][:1].upper() + c["item_sg"][1:], R.REG_COL["holder"],
            c["field"][:1].upper() + c["field"][1:]]
    if S["has_qty"]:
        cols.append(f"{c['qty'][:1].upper() + c['qty'][1:]} ({c['unit']})")
    return cols


# ------------------------------------------------------------------------------------------------ S4 notices

def notice_texts(c, S, by_n, notes=None):
    """[(ref, date, sender, receiver, text)] for every shown notice."""
    out = []
    notices = S["notices"]
    by_ref = {}
    for e in S["entries"]:
        by_ref.setdefault(e["ref"], []).append(e)
    for nt in notices:
        ref = nt["ref"]
        lines = [R.NOTICE_HEAD[c["header_v"]].format(ref=ref, d=dt_text(c, nt["date"]))]
        for e in by_ref.get(ref, []):
            body = change_body(c, S, e, by_n)
            line = R.CHANGE_PREFIX.format(ref=ref, k=e["k"]) + body
            lines.append(line)
        nt_note = (notes or {}).get(("notice", ref))
        if nt_note:
            lines.append(f"P.S. (note: {nt_note})")
        out.append((ref, nt["date"], nt["from"], nt["to"], lines))
    return out


def change_body(c, S, e, by_n):
    v = _base(c)
    if e["t"] == "WITHDRAW":
        tm = R.BODY4["WITHDRAW"]
        return tm[c["body_v"].get("VOID", 0) % len(tm)].format(m=e["target_ref"])
    if e["t"] == "CORR":
        tgt = by_n[e["target"]]
        key = "AMEND" + corr_key(e, tgt)[4:]
        v.update(m=tgt["ref"], mk=tgt["k"], s=e["value"], q=e["value"], a=e["value"], receiver=e["value"])
        return R.BODY4[key][0].format(**v)
    return body_text(c, S, e, by_n=by_n)


# ------------------------------------------------------------------------------------------------ S5 git lines

def git_line(c, S, e, by_n, hashes):
    v = _base(c)
    t = e["t"]
    if t == "CREATE":
        qtail = f" {c['qty']} {e['qty']}" if S["has_qty"] else ""
        body = R.GIT["CREATE"].format(item=e["item"], holder=e["holder"], field=c["field"], s=e["status"], qtail=qtail)
    elif t == "SET":
        key = "SET_status" if e["field"] == "status" else "SET_qty"
        body = R.GIT[key].format(item=e["item"], field=c["field"], s=e["value"], qty=c["qty"], q=e["value"])
    elif t == "ADJUST":
        body = R.GIT["ADJUST_up" if e["sign"] > 0 else "ADJUST_down"].format(item=e["item"], qty=c["qty"],
                                                                            a=e["amount"])
    elif t == "TRANSFER":
        body = R.GIT["TRANSFER"].format(item=e["item"], sender=e["sender"], receiver=e["receiver"])
    elif t == "VOID":
        body = R.GIT["VOID"].format(th=hashes[e["target"]])
    elif t == "CORR":
        tgt = by_n[e["target"]]
        k = corr_key(e, tgt)
        key = "CORR_amount" if k.startswith("CORR_amount") else k
        body = R.GIT[key].format(th=hashes[e["target"]], field=c["field"], s=e["value"], qty=c["qty"],
                                 q=e["value"], a=e["value"], receiver=e["value"])
    elif t == "SUPERSEDE":
        body = R.GIT["SUPERSEDE"].format(old=e["old"], new=e["new"])
    elif t == "OPEN":
        body = R.GIT["OPEN"].format(rec=e["record"], doc=e["doc"])
    elif t == "RENAME":
        body = R.GIT["RENAME"].format(old=e["old"], new=e["new"])
    elif t == "MERGE":
        body = R.GIT["MERGE"].format(old=e["absorbed"], new=e["survivor"])
    else:
        raise ValueError(t)
    return R.GIT_LINE.format(h=hashes[e["n"]], dt=dt_text(c, e["date"], e.get("time")), n=e["n"], body=body)


# ------------------------------------------------------------------------------------------------ stems

def _ent_ref(S, Q):
    if S["sampler"] == "S4":
        e = next(x for x in S["entries"] if x["n"] == Q["entry"])
        return R.ENT_REF["change"].format(N=e["ref"], K=e["k"])
    return R.ENT_REF["entry"].format(N=Q["entry"])


def stem_text(c, S, Q):
    """The question stem for a query in its negated stem form (2.2)."""
    kn = Q.get("kinds", False)
    Y = (c["item_sg"] + " " + Q["item"]) if (kn and Q.get("item")) else Q.get("item", "")
    X = (c["holder_sg"] + " " + Q["holder"]) if (kn and Q.get("holder")) else Q.get("holder", "")
    pt = Q.get("point") or {"kind": "end"}
    v = {"field": c["field"], "qty": c["qty"] or "", "unit": c["unit"] or "", "items": c["item_pl"],
         "hnoun": c["holder_sg"], "Y": Y, "X": X, "S": Q.get("value", ""), "CMP": Q.get("cmp", ""),
         "N": Q.get("n", ""), "END": Q.get("end_word", "at the end"), "R": Q.get("record", ""),
         "DOC": Q.get("doc", ""), "doctype": c.get("_doctype", {}).get(Q.get("doc"), "document")}
    qt, kind = Q["qt"], Q["kind"]
    if qt == "Q8":
        v["ENT"] = _ent_ref(S, Q)
        key = ("transfer", "end")
    elif qt == "Q6":
        key = ("count", "end")
    elif qt == "Q7":
        key = ("inverse", "end")
    elif qt == "Q3":
        key = ("record", "end")
    elif Q.get("still") or (qt == "Q4" and Q.get("neg") in ("N2",)) or (Q.get("neg") == "D" and Q.get("dbase") == "N2"):
        key = ("holder", "still")
    elif pt["kind"] == "range":
        key = (kind, "range")
        v["D1"], v["D2"] = dt_text(c, pt["d1"]), dt_text(c, pt["d2"])
    elif pt["kind"] == "end":
        key = (kind, "end")
    else:
        key = (kind, "date")
        v["DP"], v["D"] = pt["kind"], dt_text(c, pt["date"])
    st = R.STEM[key]
    if Q["form"] == "choice":
        return st["QC"][Q.get("qc_v", 0) % len(st["QC"])].format(**v)
    form = Q.get("neg", "A")
    if form == "A":
        if Q.get("a_frame") and "C" in st:
            return R.FRAME["A"].format(C=st["C"].format(**v))
        return st["QA"].format(**v)
    if form == "N1":
        return R.FRAME["N1"].format(Cn=st["Cn"].format(**v))
    if form == "N2":
        return R.FRAME["N2"].format(C2=R.STEM[("holder", "still")]["C2"].format(**v))
    if form == "N3":
        return st["N3"].format(**v)
    if form == "N4":
        return R.FRAME["N4"].format(C=st["C"].format(**v))
    if form == "N5":
        return R.FRAME["N5"].format(C=st["C"].format(**v))
    if form == "D":
        b = Q["dbase"]
        if b == "N1":
            cx = st["Cn"].format(**v)
        elif b == "N2":
            cx = R.STEM[("holder", "still")]["C2"].format(**v)
        else:
            cx = st["C3"].format(**v)
        return R.FRAME["D"].format(Cx=cx)
    raise ValueError(form)
