"""S7 G3 parser: reads the codebook only through the per-dataset field-value phrase lexicon and the connective
registry (AR21), the ST45 residual line, the S7 question frames (fits / choice / ATSA target frame) and the coded
text in `state`. Gold is recomputed by first fit on the parsed codebook over the source record's released
annotation (looked up by meta.text_source.record_id)."""
from __future__ import annotations

import hashlib
import json
import re

import lexicon as L
from parse import ParseError, clean_lines, strip_bullet, ws


def _lit_rx(lex):
    vals = [v["value"] for v in lex["values"]]
    names = lex.get("names") or {}
    alt = lambda xs: "(?:" + "|".join(re.escape(x) for x in sorted(xs, key=len, reverse=True)) + ")"
    out = []
    for t in lex["templates"]:
        f = t["form"]
        body = re.escape(t["template"])
        body = body.replace(re.escape("{v}"), "(?P<v>" + alt(vals) + ")")
        body = body.replace(re.escape("{c}"), "(?P<c>" + alt(vals) + ")", 1).replace(re.escape("{c}"), "(?P=c)")
        body = body.replace(re.escape("{p}"), "(?P<p>" + alt(["positive", "negative", "neutral"]) + ")")
        body = body.replace(re.escape("{f}"), "(?P<f>" + alt(list(names.values()) or vals) + ")")
        out.append((f, re.compile("^" + body + "$"), len(t["template"])))
    out.sort(key=lambda x: -x[2])
    return out, {v: k for k, v in names.items()}


def parse_lit(text, rxs, inv_names):
    for f, rx, _ in rxs:
        m = rx.match(text)
        if not m:
            continue
        neg = "-" in f
        k = f.split("+")[0].split("-")[0]
        g = m.groupdict()
        if k == "EMO":
            v = "neutral" if f.endswith("neutral") else g["v"]
            return {"op": "LIT", "atom": ["EMO", v], "neg": neg}
        if k == "PAIR":
            return {"op": "LIT", "atom": ["PAIR", g["c"], g["p"]], "neg": neg}
        if k == "CAT":
            return {"op": "LIT", "atom": ["CAT", g["c"]], "neg": neg}
        if k in ("POL", "TPOL", "OTHER"):
            return {"op": "LIT", "atom": [k, g["p"]], "neg": neg}
        if k == "FLAG":
            return {"op": "LIT", "atom": ["FLAG", inv_names.get(g["f"], g["f"])], "neg": neg}
    raise ParseError(f"S7 phrase {text[:60]!r}")


def parse_cond(text, rxs, inv):
    for op, head in (("ALL", L.LIST_HEAD["ALL"]), ("ANY", L.LIST_HEAD["ANY"])):
        if text.startswith(head + ": "):
            return {"op": op, "args": [parse_lit(x, rxs, inv) for x in text[len(head) + 2:].split(L.ITEM_SEP)]}
    return parse_lit(text, rxs, inv)


def parse_codebook(row, lex):
    rxs, inv = _lit_rx(lex)
    lines = clean_lines((row.get("card") or "") + "\n" + (row.get("instructions") or ""))
    resid = {p + "." for p in L.ST["ST45"]}
    codes, names = [], []
    for ln in lines:
        s = strip_bullet(ln)
        for qf in L.QUOTE_FORMS:
            pre, post = qf.split("{n}")
            m = re.match("^" + re.escape(pre) + r"(?P<n>[^:\n]+?)" + re.escape(post) + r": (?P<d>.+)$", s)
            if not m:
                continue
            d = m["d"]
            if d in resid:
                codes.append({"op": "RESIDUAL"})
            else:
                if not d.endswith("."):
                    break
                try:
                    codes.append(parse_cond(d[:-1], rxs, inv))
                except ParseError:
                    break
            names.append(qf.format(n=m["n"]))
            break
    if not codes or codes[-1] != {"op": "RESIDUAL"} or sum(c == {"op": "RESIDUAL"} for c in codes) != 1:
        raise ParseError("codebook: residual must be the one last code")
    return codes, names


def s7_hash(scheme, conds, query):
    return hashlib.sha256(json.dumps({"scheme": scheme, "codes": conds, "query": query}, sort_keys=True).encode()).hexdigest()


def parse_question_s7(instr, names, qtype):
    t = ws(instr)
    asked, listed = None, None
    for fr in L.ATSA_FRAME:
        rx = re.escape(fr).replace(re.escape("{T}"), "(?P<T>.+?)").replace(re.escape("{L}"), "(?P<L>.+?)")
        m = re.search(rx, t)
        if m:
            asked, listed = m["T"], m["L"].split(", ")
            break
    if qtype == "choice":
        if not any(q.replace("{E}", "") in t for q in L.Q_CHOICE["s7"]):
            raise ParseError("S7 choice question")
        return {"form": "choice", "neg": 0}, asked, listed
    from parse import _q_rx
    for q, pos, neg in L.Q_YN["fits"]:
        for lvl, frame in ((2, L.TRUTH_NEG[0].replace("{C}", neg)), (1, L.TRUTH_POS[0].replace("{C}", neg)),
                           (1, L.TRUTH_NEG[0].replace("{C}", pos)), (0, q)):
            # every start position (lookahead), so an earlier "Does ..." in an example text cannot hide the question
            rx = re.compile("(?=" + _q_rx(frame).pattern + ")")
            for m in rx.finditer(t):
                if m["X"] in names:
                    return {"form": "yn", "neg": lvl, "target": names.index(m["X"])}, asked, listed
    raise ParseError("S7 yes/no question")


def g3_s7(row, card, spec, rec):
    """Problems list for one S7 row (G3 structure + byte-for-byte text + ATSA frame; G2 first fit on the parse)."""
    import s7 as S
    probs = []
    try:
        conds, names = parse_codebook(row, card["lex"])
        q, asked, listed = parse_question_s7(row["instructions"], names, row["qtype"])
    except ParseError as e:
        return [f"parse: {e}"], None
    codes_shown = S.swapped_codes(card["codes"], *spec["swap"]) if spec.get("swap") else card["codes"]
    gen_conds = [c["condition"] if not c["residual"] else {"op": "RESIDUAL"} for c in codes_shown]
    if conds != gen_conds:
        probs.append("codebook parse differs from the structured codebook")
    if names != card["qnames"]:
        probs.append("code names differ")
    if row["state"] != rec["text"]:
        probs.append("state is not the record text byte for byte")
    ti = None
    if card["scheme"] == "mams_atsa":
        terms = rec["ann"]["terms"]
        if asked is None or listed != [t["term"] for t in terms]:
            probs.append("ATSA frame")
        else:
            hits = [i for i, t in enumerate(terms) if t["term"] == asked]
            ti = hits[0] if len(hits) == 1 else None
            if ti != spec["ti"]:
                probs.append("ATSA asked target")
        if ti is None:      # repair r1: an unresolved ATSA target is a G3 failure (the row is redrawn), never a crash
            return probs or ["ATSA asked target unresolved"], None
    if row["qtype"] == "choice":
        shown = sorted(names.index(o) for o in row["options"])
        q["shown"] = shown
        pc = [dict(code=c) for c in conds]
        g = None
        for i, c in enumerate(conds):
            if c["op"] == "RESIDUAL" or S.cond(c, rec, ti, card["scheme"]):
                g = i
                break
        gold_b = names[g] if g is not None and g in shown else None
    else:
        v = S.cond(conds[q["target"]], rec, ti, card["scheme"])
        gold_b = int(v if q["neg"] in (0, 2) else not v)
    if gold_b != row["gold"]:
        probs.append(f"G2: solver B {gold_b!r} != gold {row['gold']!r}")
    q["rec"] = rec["norm_sha256"]
    q["ti"] = ti
    h = s7_hash(card["scheme"], conds, q)
    qg = {"form": spec["form"], "neg": spec.get("neg", 0), "rec": rec["norm_sha256"], "ti": spec["ti"]}
    if spec["form"] == "choice":
        qg["shown"] = sorted(spec["options"])
    else:
        qg["target"] = spec["ask"]
    hg = s7_hash(card["scheme"], gen_conds, qg)
    if h != hg:
        probs.append("structure_hash differs")
    return probs, hg
