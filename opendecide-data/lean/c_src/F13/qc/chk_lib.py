"""Shared loaders for the independent F13 QC checker (check:F13, c-lanes-v3; structure adapted from the F12 checker's
chk_lib). Imports nothing from c_src/F13/gen or c_src/F13/solverB. Prints counts only, never row text.
Views (F13 G0 10: "G6 inputs (a)-(c) are taken from the row before card placement (question, options, card text)"):
question = instruction wording (formats-2 pool text, located verbatim in `instructions`) + the paragraph holding the
instantiated question (side `question`); card = `card` on yes/no rows, or `instructions` minus wording and question
paragraph on choice rows (the moved card text, F13R5-A1); options = option texts (+ any option-definition line in
`card`, which the model sees next to the option)."""
import ast, hashlib, json, math, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F13 = LEAN / "c_src/F13"
OUT = F13 / "out"
QC = F13 / "qc"
TMP = F13 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
POOLS = ("candidates_r1", "qc_sample", "mixdev_S5")
NEI, NONE = "not enough information", "none of the listed answers"


def _lit(v):
    if isinstance(v, str) and v[:1] in "[{(" :
        try:
            return ast.literal_eval(v)
        except Exception:
            return v
    return v


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / "side" / f"{name}.f13_meta.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l)
            side[s["id"]] = {k: _lit(v) for k, v in s.items()}
    return rows, side


def relations(name):
    p = OUT / f"relations_{name}.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() and p.stat().st_size else []


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


_W = None


def wordings():
    global _W
    if _W is None:
        _W = {}
        for l in open(LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"):
            d = json.loads(l)
            if d["id"].startswith("wd.F13.") or d.get("pool") == "F13":
                _W[d["id"]] = (d["text"], d.get("text_gb") or d["text"])
    return _W


def dio():
    if str(LEAN) not in sys.path:
        sys.path.insert(0, str(LEAN))
    import decoder_io as d
    d.STYLE, d.LAYOUT = "cygnet", "schema_branch_mark"
    if len(d.WIDE) < 100:
        U = string.ascii_uppercase
        d.WIDE = list(U) + [a + b for a in U for b in U]
    return d


def model_view(r, perm=None):
    return dio().user_msg(r, perm)


def is_yn(r):
    return r["qtype"] == "noul"


def gold_index(r):
    return r["options"].index(r["gold"])


def gold_letter(r):
    if is_yn(r):
        return "A" if r["gold"] == 1 else "B"
    return dio().label(gold_index(r))


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def _split(r, s):
    """-> (wording text or '', question paragraph without the wording, instructions with both removed)."""
    ins = r["instructions"]
    w = wordings().get(r["meta"].get("wording_id"))
    wt = ""
    if w:
        wt = w[0] if w[0] in ins else (w[1] if w[1] in ins else "")
    q = (s or {}).get("question")
    paras = ins.split("\n\n")
    if q and ins.count(q) == 1:
        qi = next(i for i, p in enumerate(paras) if q in p)
    else:
        nz = [i for i, p in enumerate(paras) if p.strip()]
        qi = next((i for i in reversed(nz) if "?" in paras[i]), nz[-1])
    qp = paras[qi]
    rest = "\n\n".join(p for i, p in enumerate(paras) if i != qi)
    if wt:
        if wt in qp:
            qp = qp.replace(wt, " ", 1)
        else:
            rest = rest.replace(wt, " ", 1)
    return wt, qp.strip(), rest.strip()


def qtext(r, s):
    wt, qp, _ = _split(r, s)
    return (wt + "\n" + qp).strip()


def views(r, s):
    wt, qp, rest = _split(r, s)
    card = (r.get("card") or "") if is_yn(r) else ""
    opts = []
    if not is_yn(r):
        d = dio().card_defs(r.get("card"))
        opts = [o + (": " + d[o] if o in d else "") for o in r["options"]]
    return {"q": (wt + "\n" + qp).strip(), "cardnoq": (card + "\n\n" + rest).strip(), "state": r["state"], "opts": opts}


def lbin(t):
    t = int(t or 0)
    return "2-4K" if t < 4000 else "4-6K" if t < 6000 else "6-7.9K"


NUM_RX = re.compile(r"-?\d+(?:[.,]\d+)?")


def as_num(o):
    t = o.strip().replace(",", "")
    m = re.fullmatch(r"[$€£¥]?\s?(-?\d+(?:\.\d+)?)(?:\s*[A-Za-z%°/][A-Za-z%°/ ]{0,19})?", t)
    return float(m.group(1)) if m else None


def n_traces(s):
    t = (s or {}).get("traces")
    return len(t) if isinstance(t, list) else 0


# Visible metadata only (FIX RULE "G6 metadata = only what the model sees"): rendered-row properties (format style,
# wording, definition style, sampler, pack, sub-type, depth, role), the question form / skill / kind (visible from the
# question), world (stated in the card), attack line present (visible in the text), question negation count,
# inner-claim negation, case location (record in the text vs case in the question), section count, number of marked
# unknowns (trace lines are visible; their class T-I / T-B / T-D is a never-feature, G0 10), lengths, numbers.
# Never used: gold, abstain_gold, trace classes, canon_sha, g12_hash, structure_hash, seed, twin_of, edge.
def meta_feats(r, s=None):
    m = r["meta"]; s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "domain_pack", "subtype")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep")); cat["role"] = str(r.get("role"))
    for k in ("skill", "kind", "form", "world", "case_loc", "inner_neg"):
        cat["sc_" + k] = str(s.get(k))
    # repair r3 (builder): the visible skill. The sidecar `skill` tags every NEI deletion twin Q-D (G0 3.1 accounting),
    # i.e. gold NEI by construction and not text-visible (G0 10 "never features", like trace class); `skill_q` is the
    # skill the question shows. Older sidecars without skill_q fall back to `skill`.
    cat["sc_skill"] = str(s.get("skill_q", s.get("skill")))
    cat["attack"] = str(m.get("twin_kind") == "attack")
    cat["lbin"] = lbin(m.get("state_tokens"))
    cat["form_x_lbin"] = cat["sc_form"] + "|" + cat["lbin"]
    num = {"len_state": float(len(r["state"])), "len_ins": float(len(r["instructions"])),
           "len_card": float(len(r.get("card") or "")), "n_lines_state": float(r["state"].count("\n")),
           "k_opts": float(len(r["options"]) if not is_yn(r) else 2), "sc_neg": float(s.get("neg") or 0),
           "state_tokens": float(m.get("state_tokens") or 0), "n_tokens": float(m.get("n_tokens") or 0),
           "n_sections": float(s.get("n_sections") or 0), "n_traces": float(n_traces(s))}
    nums = [abs(float(x.replace(",", ""))) for x in NUM_RX.findall(r["state"])][:400]
    num["state_n_numbers"] = float(len(nums)); num["state_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    qn = [abs(float(x.replace(",", ""))) for x in NUM_RX.findall(qtext(r, s))]
    num["q_n_numbers"] = float(len(qn)); num["q_max_num_log"] = math.log1p(max(qn)) if qn else 0.0
    if not is_yn(r):
        L = [len(o) for o in r["options"]]
        num["opt_len_mean"] = float(sum(L) / len(L)); num["opt_len_max"] = float(max(L))
    return cat, num


# G0 10 extra G6 / G7 features that are generator structure, not text-visible as such (decisive deciles and count,
# near-miss kinds / sub-kinds / deciles). They must not predict the label either (G0 10); gated in G7 and G10, reported
# as a G6 diagnostic (d_plus), since G6 (d) itself is visible-only.
def g0_feats(s):
    s = s or {}
    cat = {"dec_n": str(s.get("decisive_n"))}
    dd = s.get("decisive_deciles") or []
    for d in set(dd) if isinstance(dd, list) else ():
        cat[f"dec_decile_{d}"] = "1"
    nm = s.get("nm") or []
    for x in nm if isinstance(nm, list) else ():
        if isinstance(x, dict):
            cat[f"nm_kind_{x.get('kind')}"] = "1"; cat[f"nm_sub_{x.get('sub')}"] = "1"; cat[f"nm_decile_{x.get('decile')}"] = "1"
    cat["nm_count"] = str(len(nm) if isinstance(nm, list) else 0)
    return cat


def mention_pos(state, o):
    """(count, first position, last position) of whole-token occurrences of option o in the state (case-insensitive)."""
    if len(o) < 1:
        return 0, -1, -1
    ms = [m.start() for m in re.finditer(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", state, flags=re.I)]
    return (len(ms), ms[0], ms[-1]) if ms else (0, -1, -1)


def opt_kinds(r, s=None, view=None):
    """Per-option visible kind sets (choice rows): abstain kind, longest / shortest, numeric rank, mention count class in
    the document, most-mentioned, first / last mentioned in the document, named in the question, named in the card."""
    s = s or {}; v = view or views(r, s); opts = r["options"]; k = len(opts)
    out = [set() for _ in opts]
    L = [len(o) for o in opts]
    for i, o in enumerate(opts):
        if o == NEI:
            out[i].add("kind:abstain_nei")
        elif o == NONE:
            out[i].add("kind:abstain_none")
    da = [i for i, o in enumerate(opts) if o not in (NEI, NONE)]
    if da:
        mx = max(L[i] for i in da); mn = min(L[i] for i in da)
        for i in da:
            if L[i] == mx:
                out[i].add("kind:longest")
            if L[i] == mn:
                out[i].add("kind:shortest")
        nums = {i: as_num(opts[i]) for i in da}
        nums = {i: x for i, x in nums.items() if x is not None}
        if len(nums) >= 2:
            srt = sorted(set(nums.values()))
            for i, x in nums.items():
                out[i].add("kind:num_min" if x == srt[0] else "kind:num_max" if x == srt[-1] else "kind:num_mid")
        mp = {i: mention_pos(r["state"], opts[i]) for i in da}
        cmax = max(c for c, _, _ in mp.values())
        fm = [(f, i) for i, (c, f, _) in mp.items() if c]
        lm = [(l, i) for i, (c, _, l) in mp.items() if c]
        for i, (c, f, l) in mp.items():
            out[i].add("kind:mention0" if c == 0 else "kind:mention1" if c == 1 else "kind:mention2p")
            if c and c == cmax:
                out[i].add("kind:mention_max")
        if fm:
            out[min(fm)[1]].add("kind:first_in_text"); out[max(lm)[1]].add("kind:last_in_text")
        ql, cl = v["q"].lower(), v["cardnoq"].lower()
        for i in da:
            ol = opts[i].lower()
            if len(ol) >= 2 and re.search(r"(?<![\w-])" + re.escape(ol) + r"(?![\w-])", ql):
                out[i].add("kind:in_question")
            if len(ol) >= 2 and re.search(r"(?<![\w-])" + re.escape(ol) + r"(?![\w-])", cl):
                out[i].add("kind:in_card")
    return out
