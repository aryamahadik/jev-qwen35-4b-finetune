"""F11 G7 features from the model-visible text only (F11 G0 6, A22, A40, K14, F11-R2-09/12/18, R18, F11-R5-A1).
Independent F11 checker (check:F11); imports nothing from gen/ or solverB/."""
import re
import chk_lib as L

STOP = set("""a an and are as at be by code codes for from has have in is it its of on one or that the this to was
were with when only use no other any not fits list item items group named target others""".split())
ASK_RX = re.compile(r"(?:gets? code|belong to|belongs to) (.+?)(?: for the target '[^']*')?\?")
NEG_RX = re.compile(r"(?i)\b(not|no|never|none|nor|neither|without|lacks?|lacked|failed to|fails to)\b|n't\b")
WORD = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def cwords(s):
    return {w for w in WORD.findall(s.lower()) if len(w) >= 3 and w not in STOP}


def in_state(words, st):
    sw = set(WORD.findall(st.lower()))
    return sum(1 for w in words if w in sw)


def marked(lines, i):
    """own mark on the card line, or a mark on the nearest group heading line above it."""
    if i < 0:
        return False, False
    own = bool(L.MARK_RX.search(lines[i]))
    grp = False
    for j in range(i - 1, -1, -1):
        if lines[j].lower().startswith(("group ", "section ", "heading ")):
            grp = bool(L.MARK_RX.search(lines[j])); break
    return own, grp


def worked_codes(r):
    v = L.views(r)["cardnoq"]
    return set(m.strip() for m in re.findall(r"Answer key:\s*([^\n]+)", v)) | \
        set(m.strip() for m in re.findall(r"Example of ([^:\n]+):", v))


def yn_feats(r):
    st = r["state"]; q = L.views(r)["qsent"]; m = ASK_RX.search(q); f = set()
    f.add("f11:neg_in_report=" + str(bool(NEG_RX.search(st))))
    if not m:
        f.add("f11:asked=unparsed"); return f
    a = m.group(1).strip().strip("'\""); lines = L.card_lines(r); i, ln = L.option_card_line(r, a, lines)
    own, grp = marked(lines, i)
    f.add(f"f11:asked_marked_own={own}"); f.add(f"f11:asked_marked_group={grp}")
    f.add(f"f11:asked_marked_any={own or grp}")
    f.add(f"f11:asked_in_report={L.wb_find(st, a) >= 0}")
    f.add(f"f11:asked_name_word_in_report={in_state(cwords(a), st) > 0}")
    vals = cwords(ln.split(":", 1)[1]) if ":" in ln else set()
    f.add(f"f11:asked_value_mentions={min(3, in_state(vals, st))}")
    pos = [k for k, s in enumerate(lines) if re.match(r"^[A-Z0-9]", s) and ":" in s]
    if i >= 0 and pos:
        f.add(f"f11:asked_list_first={i == pos[0]}"); f.add(f"f11:asked_list_last={i == pos[-1]}")
    f.add(f"f11:asked_in_worked={a in worked_codes(r)}")
    return f


def opt_feats(r):
    opts = r["options"]; st = r["state"]; lines = L.card_lines(r); out = [set() for _ in opts]
    found = [L.option_card_line(r, o, lines) for o in opts]
    idx = [i for i, _ in found if i >= 0]
    toks = [cwords(s) for _, s in found]
    wk = worked_codes(r)
    ov = name_overlap(r, found) if not short(r) else [0] * len(opts)
    for j, o in enumerate(opts):
        i, ln = found[j]
        if i >= 0 and idx:
            if i == min(idx): out[j].add("f11:card_list_first")
            if i == max(idx): out[j].add("f11:card_list_last")
        if re.search(r"(?i)use only when|no other .* fits|not covered by|residual", ln):
            out[j].add("f11:residual")
        own, grp = marked(lines, i)
        if own: out[j].add("f11:marked_own")
        if own or grp: out[j].add("f11:marked_any")
        if L.wb_find(st, o) >= 0 and not st.lstrip().startswith(o): out[j].add("f11:written_in_report")
        if o in wk or any(o.startswith(w + " ") or w.startswith(o + " ") for w in wk): out[j].add("f11:worked_or_example")
    if max(ov or [0]) > 0:
        for j, x in enumerate(ov):
            if x == max(ov): out[j].add("f11:max_overlap_name")
    conn = []
    for j in range(len(opts)):
        conn.append(sum(len(toks[j] & toks[t]) / max(1, len(toks[j] | toks[t])) for t in range(len(opts)) if t != j)
                    if toks[j] else -1)
    if max(conn or [-1]) > 0:
        for j, c in enumerate(conn):
            if c == max(conn): out[j].add("f11:most_connected")
    if r["meta"].get("subtype") == "inverted":
        pos = [st.find(o) for o in opts]; ok = sorted(p for p in pos if p >= 0)
        for j, p in enumerate(pos):
            if p >= 0 and ok:
                if p == ok[0]: out[j].add("f11:inv_report_first")
                if p == ok[-1]: out[j].add("f11:inv_report_last")
    return out


ID_RX = re.compile(r"^[A-Z]{1,3}\d{1,3}[A-Z]?$|^[A-Z]\d[A-Z]$")


def short(r):
    return "short_card" in (r["meta"].get("edge") or [])


NAME_RX = re.compile(r"^[A-Z][a-z]+(?: [A-Z][a-z]+){0,3}$")


def code_name(o, line):
    """the code's name: the option itself in name form; for an ID option, the capitalised 1-4 word label written next
    to the ID on its card line ('ID Name: ...', '| ID | Name | ...'); '' when the card gives the code no name."""
    if not ID_RX.match(o.strip()):
        return o
    k = line.find(o)
    if k < 0:
        return ""
    rest = line[k + len(o):].lstrip(" |")
    cand = re.split(r"[:|(=]", rest, 1)[0].strip()
    return cand if NAME_RX.match(cand) else ""


def name_overlap(r, found):
    """R18 full cards: number of content words of the option's NAME that occur in the report as whole words. An ID
    option's name is looked up on every card line holding the ID (decision lists name codes on separate lines)."""
    st = r["state"]; lines = L.card_lines(r); out = []
    for o, (i, ln) in zip(r["options"], found):
        nm = code_name(o, ln)
        if not nm and ID_RX.match(o.strip()):
            for x in lines:
                if L.wb_find(x, o) >= 0:
                    nm = code_name(o, x)
                    if nm:
                        break
        out.append(in_state(cwords(nm), st) if nm else 0)
    return out


def subj_sents(st):
    """report sentences after the subject line."""
    lines = [x for x in st.split("\n") if x.strip()]
    k = next((i for i, x in enumerate(lines) if re.search(r"(?i)^\W*(subject|re|ref|unit|file)\s*:", x)), -1)
    body = " ".join(lines[k + 1:]) if k >= 0 else " ".join(lines)
    return [x for x in L.SENT_RX.split(body) if x.strip()]


def short_slice(r):
    """F11 G0 6 short-card slice: tied-at-max value-name overlap set T; per tied option, whether its distinguishing
    value name first appears in the first / last sentence after the subject line. -> (T indices, {feat: set(idx)})"""
    opts = r["options"]; st = r["state"].lower()
    vals = [[v.strip().lower() for v in re.sub(r"\s*\[[^\]]*\]\s*$", "", o).split(" / ")] for o in opts]
    ov = [sum(1 for v in vs if L.wb_find(st, v) >= 0) for vs in vals]
    if not ov or max(ov) == 0:
        return [], {}
    T = [j for j, x in enumerate(ov) if x == max(ov)]
    common = set.intersection(*[set(vals[j]) for j in T]) if T else set()
    sents = [x.lower() for x in subj_sents(r["state"])]
    feats = {"f11s:first_sent": set(), "f11s:last_sent": set()}
    for j in T:
        d = [v for v in vals[j] if v not in common and L.wb_find(st, v) >= 0]
        if not d or not sents:
            continue
        si = min((i for i, x in enumerate(sents) if any(L.wb_find(x, v) >= 0 for v in d)), default=-1)
        if si == 0: feats["f11s:first_sent"].add(j)
        if si == len(sents) - 1 and si >= 0: feats["f11s:last_sent"].add(j)
    return T, feats
