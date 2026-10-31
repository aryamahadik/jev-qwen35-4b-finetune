"""Shared loaders for the independent F12 QC checker (check:F12, c-lanes-v3; adapted from the F9 checker's chk_lib).
Imports nothing from c_src/F12/gen or c_src/F12/solverB. Prints counts only, never row text.
Views follow F12 G0 8 ("Shortcut inputs on choice rows", A16.1 g): the question-only input is the instruction wording
(formats-2 pool text, located verbatim in `instructions`) plus the paragraph holding the instantiated question (side
`question`, which occurs exactly once in `instructions`); the card-only input is the card text wherever it sits (`card`
on yes/no rows; the moved card text = `instructions` minus wording and question paragraph on choice rows);
option-definition lines (the `card` field of choice rows) belong to the options input; C-INV candidate requests sit in
`state` (text input)."""
import hashlib, json, math, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F12 = LEAN / "c_src/F12"
OUT = F12 / "out"
QC = F12 / "qc"
TMP = F12 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
POOLS = ("candidates_r1", "qc_sample", "mixdev_S5")


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / "side" / f"{name}.side.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
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
            if d["id"].startswith("wd.F12.") or d.get("pool") == "F12":
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
    """Exactly what the model sees: decoder_io.user_msg under cygnet + schema_branch_mark."""
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


ABSTAIN = {"None of the listed tools can do this": "tool_none", "Nothing is missing": "param_nothing",
           "No usable value, so ask the user": "value_none", "Nothing, the call is valid": "defect_nothing"}
ACT_FIXED = {"Say it cannot be done": "act_unable", "Answer directly from what is shown": "act_answer"}


def abstain_kind(o):
    return ABSTAIN.get(o.strip())


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


NUM_RX = re.compile(r"-?\d+(?:[.,]\d+)?")


def as_num(o):
    t = o.strip().replace(",", "")
    m = re.fullmatch(r"[$€£¥]?\s?(-?\d+(?:\.\d+)?)(?:\s*[A-Za-z%°/][A-Za-z%°/ ]{0,19})?", t)
    return float(m.group(1)) if m else None


# Visible metadata only (FIX RULE "G6 metadata = only what the model sees"). meta fields that describe the rendered
# row (format style, wording, definition style, sampler, pack, question form = subtype, depth, attacked role) and side
# fields that are visible properties of the rendered prompt: layout (catalog layout), card_mode, form, framing (P / N
# question wording), request cue class (G0 8 "request kind cue"), negation count of the question, catalog size, records /
# turns / stored results / proposed call / role line present, statement types shown in the conversation, card policy
# settings (stated in the card), mask / swap scheme (option names), real token length. Never used (hidden or
# label-derived): outcome, tool, near_miss, gold_canon, opts_canon, card_free_ok, must_show, audit, cases, rel,
# twin_kind, edge, structure_hash, seed, kind (action / info / catalog: the semantic request type that decides the
# outcome, not metadata).
def meta_feats(r, s=None):
    m = r["meta"]; s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "domain_pack", "subtype")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep")); cat["role"] = str(r.get("role"))
    for k in ("layout", "card_mode", "form", "framing"):
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    nm = s.get("names")
    cat["sc_names"] = str(nm.get("scheme")) if isinstance(nm, dict) else "plain"
    S = s.get("S") or {}
    pol = S.get("pol") or {}
    for k, v in sorted(pol.items()):
        cat["pol_" + k] = str(v)
    conv = S.get("conv") or []
    types = sorted({st.get("t") for t in conv for st in (t.get("st") or []) if isinstance(st, dict)})
    for t in types:
        cat["st_" + str(t)] = "1"
    cues = sorted({str(st.get("cue")) for t in conv for st in (t.get("st") or []) if isinstance(st, dict) and st.get("t") == "req"})
    cat["req_cue"] = "+".join(cues)
    cat["role_line"] = str(S.get("role") is not None)
    num = {"len_state": float(len(r["state"])), "len_ins": float(len(r["instructions"])),
           "len_card": float(len(r.get("card") or "")), "n_lines_state": float(r["state"].count("\n")),
           "k_opts": float(len(r["options"]) if not is_yn(r) else 2),
           "sc_neg": float(s.get("neg") or 0), "sc_catalog_n": float(s.get("catalog_n") or len(S.get("tools") or [])),
           "sc_real_tokens": float(s.get("real_tokens") or -1), "n_records": float(len(S.get("records") or [])),
           "n_turns": float(len(conv)), "n_user_turns": float(sum(t.get("who") == "user" for t in conv)),
           "n_stored": float(len(S.get("stored") or [])), "call_shown": float(S.get("call") is not None)}
    nums = [abs(float(x.replace(",", ""))) for x in NUM_RX.findall(r["state"])][:200]
    num["state_n_numbers"] = float(len(nums)); num["state_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    qn = [abs(float(x.replace(",", ""))) for x in NUM_RX.findall(qtext(r, s))]
    num["q_n_numbers"] = float(len(qn)); num["q_max_num_log"] = math.log1p(max(qn)) if qn else 0.0
    if not is_yn(r):
        L = [len(o) for o in r["options"]]
        num["opt_len_mean"] = float(sum(L) / len(L)); num["opt_len_max"] = float(max(L))
    return cat, num


def first_pos(state, o):
    """character position of the first whole-token occurrence of option o in the state, -1 if absent."""
    if len(o) < 2:
        return -1
    m = re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", state)
    return m.start() if m else -1
