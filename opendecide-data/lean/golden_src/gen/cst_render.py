"""Rendering of gen_constraints instances into the state text (8 layouts x 9 option formats x per-domain contexts).

render(inst, st) -> (state, rec).  rec holds, for the independent verifier, every option's displayed strings and the
text segment they must appear in, each requirement's rendered text, the tie-break sentence and the notes.
All random surface choices live in the style dict st (drawn once per fact-flip pair) so both twins share them.
"""
import csv
import io

from cst_core import MISSING, NA, cap, unk

LAYOUTS = ["brief", "email", "ticket", "chat", "policy", "fields", "optfirst", "narrative"]
LAYOUT_W = [16, 14, 11, 10, 11, 11, 12, 15]
FORMATS = ["md", "pipe", "csv", "bullets", "cards", "prose", "fixed", "trans", "numbered"]
FORMAT_W = [16, 10, 7, 14, 11, 14, 9, 7, 12]
FIRST_PERSON = {"email", "ticket", "chat"}
TABLE_FORMATS = {"md", "pipe", "csv", "fixed", "trans"}
REQ_HEADS = ["Requirements:", "Must-haves:", "Hard requirements:", "It has to meet all of these:", "Conditions:"]
MISSING_TOKENS = ["not stated", "unknown", "TBC", "not listed"]
MISS_RULES = ['Anything marked "{t}" has not been confirmed and does not count as meeting a requirement.',
              'Treat "{t}" as not meeting whatever requirement that detail is needed for.',
              'If a detail shows "{t}", assume it does not meet the requirement.']
NOTE_TPL = ["Update: {L} now {p}.", "Correction to the list above: {L} now {p}.",
            "Late change (not yet reflected in the list): {L} now {p}."]
INTROS = ["Options:", "Here is what I found:", "Shortlist:", "The {plural} under consideration:"]
ORGS = ["Operations", "Facilities", "Procurement", "Office Services", "Travel Desk", "Admin Team"]


def join_and(xs):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def draw_style(rng, D, n_cons, n_opts):
    fmts = list(FORMATS)
    w = list(FORMAT_W)
    if n_opts > 6:
        w[fmts.index("trans")] = 0
    st = {
        "layout": rng.choices(LAYOUTS, weights=LAYOUT_W)[0],
        "fmt": rng.choices(fmts, weights=w)[0],
        "time": rng.choice(["24", "24", "12"]),
        "date": rng.choice(["dmy", "mdy", "iso", "long"]),
        "bool": rng.choice(["yn", "YN", "yx"]),
        "dur": rng.choice(["hm", "hm", "min", "colon"]),
        "cur": getattr(D, "cur_fixed", None) or rng.choice(["$", "$", "$", "€", "£"]),
        "missing": rng.choice(MISSING_TOKENS),
        "na": rng.choice(["—", "n/a"]),
        "mi": [rng.randrange(3) for _ in range(n_cons + 2)],
        "ctx_i": rng.randrange(60), "q_i": rng.randrange(60), "intro_i": rng.randrange(60), "subj_i": rng.randrange(60),
        "tie_i": rng.randrange(60), "head_i": rng.randrange(60), "miss_i": rng.randrange(60), "note_i": rng.randrange(60),
        "bullet": rng.choice(["-", "-", "•", "*"]),
        "sender_last": rng.choice(["Okafor", "Lindqvist", "Moreau", "Haddad", "Novak", "Brennan", "Mensah", "Varga"]),
        "recipient": rng.choice(["Sam", "Alex", "Jordan", "Robin", "Casey", "Morgan", "Taylor", "Jamie"]),
        "ticket": rng.randint(1000, 99999), "org": rng.choice(ORGS), "reqstyle": rng.random(),
    }
    return st


def cell(inst, st, i, a):
    A = inst["D"].A[a]
    v = inst["shown"].get((i, a), inst["opts"][i].get(a, MISSING))
    return A.fmt(v, st)


def shown_value(inst, i, a):
    return inst["shown"].get((i, a), inst["opts"][i].get(a, MISSING))


def show_attrs(inst, rng_extra):
    """Displayed columns: every attribute a requirement or the tie-break uses, the domain's always-shown ones, plus
    1-2 distractor columns; in the domain's declared order."""
    D = inst["D"]
    need = set(D.always)
    for c in inst["cons"]:
        need.update(c.attrs)
        for node_attr in getattr(c, "shows", ()):
            need.add(node_attr)
    if inst["tie"]:
        need.update(inst["tie"].attrs)
    if inst.get("nice"):
        need.add(inst["nice"])
    need.update(rng_extra)
    out = []
    for a in D.attrs:
        if a.key in need and not (a.derived and a.key not in D.always):
            out.append(a.key)
    return out


def options_block(inst, st, cols):
    D = inst["D"]
    hv = st.get("hv", {})
    labels = inst["labels"]
    n = len(labels)
    heads = [D.A[a].header.format(**hv) for a in cols]
    cells = [[cell(inst, st, i, a) for a in cols] for i in range(n)]
    f = st["fmt"]
    segs, lines = [], []
    rec_cells = [{a: cells[i][k] for k, a in enumerate(cols)} for i in range(n)]
    trans_rows = None
    if f == "md":
        lines.append("| " + " | ".join([D.head] + heads) + " |")
        lines.append("|" + "|".join(["---"] * (len(cols) + 1)) + "|")
        for i in range(n):
            s = "| " + " | ".join([labels[i]] + cells[i]) + " |"
            lines.append(s)
            segs.append(s)
    elif f == "pipe":
        lines.append(" | ".join([D.head] + heads))
        for i in range(n):
            s = " | ".join([labels[i]] + cells[i])
            lines.append(s)
            segs.append(s)
    elif f == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow([D.head] + heads)
        for i in range(n):
            w.writerow([labels[i]] + cells[i])
        lines = buf.getvalue().rstrip("\n").split("\n")
        segs = lines[1:]
    elif f == "fixed":
        rows = [[D.head] + heads] + [[labels[i]] + cells[i] for i in range(n)]
        wd = [max(len(r[k]) for r in rows) for k in range(len(rows[0]))]
        fmt_row = lambda r: "  ".join(x.ljust(wd[k]) for k, x in enumerate(r)).rstrip()
        lines.append(fmt_row(rows[0]))
        lines.append("  ".join("-" * wd[k] for k in range(len(wd))))
        for i in range(n):
            s = fmt_row(rows[i + 1])
            lines.append(s)
            segs.append(s)
    elif f == "trans":
        lines.append(" | ".join([D.head] + labels))
        trans_rows = {}
        for k, a in enumerate(cols):
            s = " | ".join([heads[k]] + [cells[i][k] for i in range(n)])
            lines.append(s)
            trans_rows[a] = s
        segs = ["\n".join(lines)] * n
    elif f == "bullets":
        for i in range(n):
            s = f"{st['bullet']} {labels[i]}: " + "; ".join(f"{heads[k]}: {cells[i][k]}" for k in range(len(cols)))
            lines.append(s)
            segs.append(s)
    elif f == "numbered":
        for i in range(n):
            s = f"{i + 1}. {labels[i]} — " + " | ".join(f"{heads[k]}: {cells[i][k]}" for k in range(len(cols)))
            lines.append(s)
            segs.append(s)
    elif f == "cards":
        for i in range(n):
            blk = [labels[i]] + [f"  {heads[k]}: {cells[i][k]}" for k in range(len(cols))]
            s = "\n".join(blk)
            lines.append(s + "\n")
            segs.append(s)
        lines[-1] = lines[-1].rstrip("\n")
    elif f == "prose":
        for i in range(n):
            ph = []
            for k, a in enumerate(cols):
                A = D.A[a]
                v = shown_value(inst, i, a)
                p = A.prose(v, st)
                ph.append(p)
                rec_cells[i][a] = p if (A.kind == "bool" and not unk(v)) or (A.kind == "set" and not unk(v) and not v) \
                    else cells[i][k]
            s = f"{labels[i]} {join_and(ph)}."
            lines.append(s)
            segs.append(s)
    else:
        raise ValueError(f)
    return "\n".join(lines), segs, rec_cells, trans_rows


def req_block(inst, st, voice, style):
    D = inst["D"]
    rs = [c.render(st, st["mi"][j]) for j, c in enumerate(inst["cons"])]
    texts = []
    if style in ("bullets", "numbered", "fields"):
        items = []
        for r in rs:
            if style == "fields" and r.get("field"):
                items.append(r["field"])
            else:
                items.append(r.get("sentence") or r["bullet"])
        if style == "numbered":
            lines = [f"{k + 1}. {x}" for k, x in enumerate(items)]
        else:
            lines = [f"{st['bullet']} {x}" if style == "bullets" else x for x in items]
        texts = items
        return "\n".join(lines), texts
    subj = "It" if (voice == "first" and not getattr(D, "person", False)) else f"The {D.noun}"
    simple = [r for r in rs if not r.get("compound")]
    comp = [r for r in rs if r.get("compound")]
    sents = []
    if simple:
        s = f"{subj} {join_and([r['inline'] for r in simple])}."
        sents.append(s)
    for r in comp:
        if r.get("sentence"):
            sents.append(r["sentence"])
        else:
            sents.append(f"{subj} {r['inline']}.")
    texts = [r.get("sentence") if (r.get("compound") and r.get("sentence")) else r["inline"] for r in rs]
    return " ".join(sents), texts


def render(inst, st):
    D, ctx = inst["D"], inst["ctx"]
    st = dict(st)
    st["hv"] = D.hv(ctx) if D.hv else {}
    cs = D.cs(ctx, st)
    cs["ifany"] = ", if any" if inst["none_opt"] else ""
    cs["noun"], cs["plural"] = D.noun, D.plural
    lay = st["layout"]
    voice = "first" if lay in FIRST_PERSON else "third"
    f1, f3 = D.contexts[st["ctx_i"] % len(D.contexts)]
    context = (f1 if voice == "first" else f3).format(**cs)
    context = cap(context)
    csents = [c.ctx_sentence(st, st["mi"][j]) for j, c in enumerate(inst["cons"])]
    csents = [x for x in csents if x]
    ctx_text = " ".join([context] + csents)
    # requirement style
    if lay in ("brief",):
        rstyle = "bullets" if st["reqstyle"] < 0.6 else "numbered"
    elif lay in ("ticket", "policy"):
        rstyle = "numbered"
    elif lay == "fields":
        rstyle = "fields"
    else:
        rstyle = "paragraph"
    req_text, req_items = req_block(inst, st, voice, rstyle)
    tie_text = inst["tie"].texts[st["tie_i"] % len(inst["tie"].texts)] if inst["tie"] else ""
    nice_text = ""
    if inst.get("nice"):
        A = D.A[inst["nice"]]
        nice_text = f"Nice to have, but not required: {A.header.format(**st['hv']).lower()}."
    # rules for unknown / not-applicable cells
    cols = inst["cols"]
    shown_vals = [shown_value(inst, i, a) for i in range(len(inst["labels"])) for a in cols]
    rules = []
    if st.get("force_missing_rule") or any(v == MISSING for v in shown_vals):
        rules.append(MISS_RULES[st["miss_i"] % len(MISS_RULES)].format(t=st["missing"]))
    if any(v == NA for v in shown_vals):
        rules.append(f'"{st["na"]}" means the detail does not apply.')
    rules_text = " ".join(rules)
    opts_text, segs, rec_cells, trans_rows = options_block(inst, st, cols)
    notes = []
    for (i, a) in inst["notes"]:
        A = D.A[a]
        v = inst["opts"][i][a]
        p = A.prose(v, st)
        notes.append((i, a, NOTE_TPL[st["note_i"] % len(NOTE_TPL)].format(L=inst["labels"][i], p=p),
                      p if A.kind in ("bool",) or (A.kind == "set" and not v) else A.fmt(v, st)))
    notes_text = "\n".join(x[2] for x in notes)
    intros = D.intros + INTROS
    intro = intros[st["intro_i"] % len(intros)].format(**cs)
    head = REQ_HEADS[st["head_i"] % len(REQ_HEADS)]
    first_name = ctx["name"]
    full = f"{first_name} {st['sender_last']}"
    subj = (D.subjects[st["subj_i"] % len(D.subjects)] if D.subjects else "Quick question").format(**cs)
    opt_part = opts_text + ("\n\n" + notes_text if notes_text else "")
    blocks = []
    if lay == "brief":
        blocks = [ctx_text, head + "\n" + req_text + ("\n" + tie_text if tie_text else "") +
                  ("\n" + nice_text if nice_text else ""), rules_text, intro + "\n" + opt_part]
    elif lay == "email":
        body = " ".join(x for x in [ctx_text, req_text, tie_text, nice_text] if x)
        blocks = [f"From: {full}\nTo: {st['recipient']}\nSubject: {cap(subj)}", f"Hi {st['recipient']},", body,
                  intro, opt_part, rules_text, f"Thanks,\n{first_name}"]
    elif lay == "ticket":
        t = f"Request #{st['ticket']} ({st['org']})\nSubmitted by: {full}\nSummary: {context}"
        if csents:
            t += "\nDetails: " + " ".join(csents)
        t += "\nHard requirements:\n" + req_text
        t += "\nTie-break: " + (tie_text if tie_text else "none given")
        if nice_text:
            t += "\n" + nice_text
        blocks = [t, rules_text, intro + "\n" + opt_part]
    elif lay == "chat":
        blocks = [f"{first_name}: {ctx_text}\n{first_name}: {req_text}" + (f" {tie_text}" if tie_text else "") +
                  (f" {nice_text}" if nice_text else "") + f"\n{first_name}: {intro}", opt_part, rules_text]
    elif lay == "policy":
        blocks = [f"{st['org']}: selection rule for {D.plural}\n{ctx_text}",
                  f"A {D.noun} may be chosen only if it meets every one of these conditions:\n{req_text}" +
                  (f"\n{tie_text}" if tie_text else ""), rules_text, intro + "\n" + opt_part]
    elif lay == "fields":
        blocks = [ctx_text, req_text + (f"\n{tie_text}" if tie_text else "") + (f"\n{nice_text}" if nice_text else ""),
                  rules_text, opt_part]
    elif lay == "optfirst":
        blocks = [intro + "\n" + opt_part, " ".join(x for x in [ctx_text, req_text, tie_text, nice_text, rules_text] if x)]
    elif lay == "narrative":
        blocks = [" ".join(x for x in [ctx_text, req_text, tie_text, nice_text] if x), intro + "\n" + opt_part,
                  rules_text]
    state = "\n\n".join(b for b in blocks if b and b.strip())
    qs = D.questions
    question = qs[st["q_i"] % len(qs)].format(**cs)
    rec = {"segs": segs, "cells": rec_cells, "trans_rows": trans_rows, "req_items": req_items, "tie_text": tie_text,
           "notes": notes, "ctx_sents": csents, "cols": cols, "rules": rules, "question": question}
    return state, question, rec
