"""Per-row feature extraction for the golden_train profile and the dev error breakdown (read-only)."""
import ast, hashlib, json, os, re, sys

LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
sys.path.insert(0, LEAN)
os.environ.setdefault("OD_STYLE", "cygnet")
import decoder_io as D  # noqa: E402

D.STYLE = "cygnet"
D.LAYOUT = "schema_branch_mark"

YESNO = re.compile(r"\byes\s*(,|or|/)\s*no\b|\byes\b\s*/\s*\bno\b", re.I)
QUOTED = re.compile(r"\"[^\"]{0,200}\"|“[^”]{0,200}”")
SYN = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot)\b|n't\b", re.I)
LEX = re.compile(r"\b(wrong|incorrect|false|untrue|inaccurate|reject|rejected|rule[sd]? out|ruling out|deny|denies|denied|"
                 r"fail|fails|failed|lack|lacks|lacking|absent|absence|unlikely|impossible|invalid|disagree|refute|refutes|"
                 r"contradict|contradicts|mistaken|exclude|excluded|unable|unless|except|nowhere|unsupported|mistake|"
                 r"dispute|disputes|doubt)\b", re.I)
NEI = re.compile(r"not enough|insufficient|cannot be determined|can't be determined|cannot tell|can't tell|undetermined|"
                 r"\bunknown\b|\bunclear\b|not mentioned|not stated|not given|unanswerable|not specified|unverifiable|"
                 r"no answer|cannot be answered|not answerable|undecidable|not determinable|insufficient information|"
                 r"no information", re.I)
NEUTRAL = re.compile(r"\bneutral\b|\bneither\b", re.I)
NONEOF = re.compile(r"none of (the|these|them)|\bother\b|out of scope|out-of-scope|no intent|\bno label\b", re.I)
RISK = re.compile(r"\b(will|likely|likelihood|risk|risky|probab\w*|chance|predict\w*|expected to|going to|forecast\w*|"
                  r"outcome|end up|succeed|severity|hazard\w*)\b", re.I)
TOOLS = re.compile(r"\b(function call|tool call|api call|call the|which tool|which function|which api|endpoint|"
                   r"function_call|tool_call|tools?:|functions?:)\b|\"(parameters|arguments)\"\s*:", re.I)
DIFF = re.compile(r"^(diff --git|@@ -\d|\+\+\+ b/|--- a/)", re.M)
CODE = re.compile(r"^\s*(def \w+\(|class \w+[(:]|function \w*\(|#include|import \w+|from \w+ import|public (static )?\w+|"
                  r"const \w+ =|let \w+ =|var \w+ =|return [^.]*;\s*$|\}\s*$)", re.M)
DIAL = re.compile(r"^\s*(user|customer|agent|assistant|system|human|bot|ai|speaker\s*\w*|client|caller|operator|"
                  r"representative|rep|support|patient|doctor|usr|sys|person [ab]|[ab]|q|a|interviewer|host|guest)\s*:",
                  re.I | re.M)
EMAIL = re.compile(r"^(subject|from|to|sent|date|cc)\s*:", re.I | re.M)
HTML = re.compile(r"<(p|div|br|table|span|a|li|ul|td|tr|h\d)\b[^>]*>", re.I)
KV = re.compile(r"^[A-Za-z][\w /()'.,&-]{0,40}:\s+\S", re.M)
BUL = re.compile(r"^\s*([-*•]|\d+[.)])\s+\S", re.M)
NUM = re.compile(r"\d+(?:[.,]\d+)?")
ORD = re.compile(r"^(\d{1,2}|very \w+|extremely \w+|low|medium|moderate|high|severe|minor|major|critical|mild|none|"
                 r"slight\w*|strong\w*|weak\w*|somewhat \w+|not at all|a little|a lot|always|never|often|rarely|"
                 r"sometimes|level \w+|grade \w+|tier \w+|ef\d)\b", re.I)


def pmeta(m):
    if isinstance(m, dict):
        return m
    if not m:
        return {}
    try:
        return ast.literal_eval(m)
    except Exception:
        try:
            return json.loads(m)
        except Exception:
            return {}


def popts(o):
    if o is None or isinstance(o, list):
        return o
    if isinstance(o, str):
        if o == "None":
            return None
        try:
            return ast.literal_eval(o)
        except Exception:
            return None
    return None


def neg_counts(text):
    t = YESNO.sub(" ", text or "")
    t = QUOTED.sub(" Q ", t)
    return len(SYN.findall(t)), len(LEX.findall(t))


def fmt_of(st):
    lines = st.splitlines()
    pipe = sum(1 for l in lines if l.count("|") >= 2)
    tabs = sum(1 for l in lines if l.count("\t") >= 2)
    flags = {
        "diff": bool(DIFF.search(st)),
        "code": len(CODE.findall(st)) >= 3,
        "json": bool(re.match(r"\s*[\{\[]", st)) and '":' in st,
        "table": pipe >= 2 or tabs >= 2,
        "dialogue": len(DIAL.findall(st)) >= 2,
        "email": len(EMAIL.findall(st)) >= 2,
        "html": len(HTML.findall(st)) >= 2,
        "kv": len(KV.findall(st)) >= 3,
        "bullets": len(BUL.findall(st)) >= 3,
    }
    prim = "prose"
    for k in ("diff", "code", "json", "table", "dialogue", "email", "html", "kv", "bullets"):
        if flags[k]:
            prim = k
            break
    return prim, flags


def jacc_max(opts):
    if not opts or len(opts) < 2 or len(opts) > 60:
        return None
    sets = [set(re.findall(r"[a-z0-9]+", o.lower())) for o in opts]
    best = 0.0
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            a, b = sets[i], sets[j]
            if a and b:
                v = len(a & b) / len(a | b)
                if v > best:
                    best = v
    return round(best, 3)


def features(r):
    md = pmeta(r.get("meta"))
    opts = popts(r.get("options"))
    st = r.get("state") or ""
    ins = r.get("instructions") or ""
    card = r.get("card") or ""
    q = r["qtype"]
    f = {"id": r["id"], "source": r.get("source"), "track": r.get("track"), "role": r.get("role"), "qtype": q,
         "group_id": r.get("group_id"),
         "family": md.get("family"), "domain": md.get("domain"), "teacher": int("teacher" in md),
         "edge": md.get("edge") or "", "attack": int(bool(md.get("attack_target")) or r.get("role") == "attacked"
                                                       or bool(md.get("arm"))),
         "near_miss": int(bool(md.get("near_miss"))), "renamed": int(bool(md.get("renamed"))),
         "defswap": int("defswap" in md), "twin": int(bool(md.get("twin_of") or md.get("twin_id"))),
         "container": md.get("container") or ""}
    f["state_chars"] = len(st)
    f["state_words"] = len(st.split())
    f["card_chars"] = len(card)
    f["has_card"] = int(len(card.strip()) > 0)
    f["ins_chars"] = len(ins)
    lines = [l for l in ins.strip().splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    f["ins_lines"] = len(lines)
    if q == "noul":
        if re.search(r'^Is the correct answer "', last):
            yf = "label_aff"
        elif re.search(r'^Is it wrong to answer "', last):
            yf = "label_neg"
        elif len(lines) >= 2 and re.search(r'"[^"]+"', last):
            yf = "label_other"
        else:
            yf = "natural"
        f["ynform"] = yf
        f["yn_gold"] = int(r.get("gold") == 1) if r.get("gold") in (0, 1) else None
    else:
        f["ynform"] = ""
        f["yn_gold"] = None
    s, l = neg_counts(last if q == "noul" else ins)
    f["neg_syn"], f["neg_lex"] = s, l
    s2, l2 = neg_counts(ins)
    f["neg_all_ins"] = s2 + l2
    m = QUOTED.findall(last)
    f["asked_label_neg"] = int(any(SYN.search(x) for x in m))
    f["state_neg"] = len(SYN.findall(st[:4000]))
    prim, flags = fmt_of(st)
    f["fmt"] = prim
    for k, v in flags.items():
        f["f_" + k] = int(v)
    first = st.lstrip().splitlines()[0] if st.strip() else ""
    f["header"] = first[:40] if (len(first) <= 40 and first.rstrip().endswith(":")) else ""
    f["nums_state"] = len(NUM.findall(st[:4000]))
    f["nonascii"] = round(sum(1 for c in st[:2000] if ord(c) > 127) / max(1, min(len(st), 2000)), 3)
    defs = D.card_defs(card)
    if q == "choice":
        f["n_opt"] = len(opts or [])
        try:
            f["gold_pos"] = (opts or []).index(r.get("gold"))
        except ValueError:
            f["gold_pos"] = -1
        texts = [o + " " + defs.get(o, "") for o in (opts or [])]
        f["opt_mean_chars"] = round(sum(len(o) for o in (opts or [])) / max(1, len(opts or [])), 1)
        f["close"] = None if f["renamed"] else jacc_max(opts)
        gold_txt = (r.get("gold") or "") + " " + defs.get(r.get("gold") or "", "")
        f["gold_nei"] = int(bool(NEI.search(gold_txt)))
        f["gold_neutral"] = int(bool(NEUTRAL.search(gold_txt)))
        f["gold_noneof"] = int(bool(NONEOF.search(r.get("gold") or "")))
        alltxt = " ".join(texts)
        f["ordinal"] = int(sum(1 for o in (opts or []) if ORD.search(o.strip())) >= max(2, len(opts or []) - 1))
    else:
        f["n_opt"] = 2
        f["gold_pos"] = None
        f["opt_mean_chars"] = None
        f["close"] = None
        f["n_card_labels"] = len(defs)
        alltxt = card
        f["gold_nei"] = f["gold_neutral"] = f["gold_noneof"] = None
        f["ordinal"] = 0
    f["n_card_labels"] = len(defs)
    f["has_nei_opt"] = int(bool(NEI.search(alltxt)) or bool(re.search(r"\bunknown\b|not enough", ins, re.I)))
    f["has_neutral_opt"] = int(bool(NEUTRAL.search(alltxt)))
    f["has_noneof_opt"] = int(bool(NONEOF.search(" ".join(opts or []))))
    f["risk_q"] = int(bool(RISK.search(ins)))
    f["tools"] = int(bool(TOOLS.search(ins)) or bool(TOOLS.search(st[:3000])))
    norm = QUOTED.sub("Q", ins.lower())
    norm = re.sub(r"\d+", "0", norm)
    f["ins_hash"] = hashlib.md5(norm.encode()).hexdigest()[:10]
    fw = re.findall(r"[A-Za-z']+", last)
    f["ins_first"] = fw[0].lower() if fw else ""
    try:
        f["prompt"] = D.user_msg(r if isinstance(r.get("options"), list) or r.get("options") is None
                                 else {**r, "options": opts})
    except Exception as e:  # pragma: no cover
        f["prompt"] = st + "\n" + ins + "\n" + card
    return f
