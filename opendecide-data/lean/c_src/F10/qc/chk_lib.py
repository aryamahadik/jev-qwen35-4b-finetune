"""Shared loaders for the independent F10 QC checker (check:F10, c-lanes-v3). Imports nothing from c_src/F10/gen or
c_src/F10/solverB. Prints counts only, never row text."""
import hashlib, json, math, random, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F10 = LEAN / "c_src/F10"
OUT = F10 / "out"
QC = F10 / "qc"
TMP = F10 / "tmp/chk"


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / f"{name}.sidecar.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
    return rows, side


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


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


def gold_letter(r):
    d = dio()
    if is_yn(r):
        return "A" if r["gold"] == 1 else "B"
    return d.label(r["options"].index(r["gold"]))


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


# ---------------------------------------------------------------- visible-text helpers (checker's own parsing)
ABSTAIN_RX = re.compile(r"(?i)^(none of (this|the) (card's|table's|codebook's)? ?(terms|codes)|none of the (terms|codes) on this "
                        r"(card|table)|no term on this card|none of this table's codes|the record does not settle it|"
                        r"not decidable from the record|cannot be determined|undetermined)")
RESID_RX = re.compile(r"(?i)(every other code|none of the (other|remaining) codes|no code earlier|codes? listed above it|"
                      r"matches no other code|no other code on this card|none of the codes above)")
NUM_RX = re.compile(r"\d+(?:\.\d+)?")


def split_q(ins):
    """question paragraph = last paragraph of `instructions` holding '?'; rest = the other paragraphs."""
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def views(r):
    q, rest = split_q(r["instructions"])
    return {"q": q, "cardnoq": ((r.get("card") or "") + "\n\n" + rest).strip(), "state": r["state"],
            "opts": list(r["options"] or [])}


def full_text(r):
    return "\n\n".join([r.get("card") or "", r["instructions"], r["state"]] + (list(r["options"]) if not is_yn(r) else []))


def def_line(r, o):
    """the visible definition line of option o (card or instructions), '' if none."""
    txt = (r.get("card") or "") + "\n" + r["instructions"]
    for ln in txt.split("\n"):
        s = ln.lstrip("-*•+> |").strip()
        if s.startswith(o) and len(s) > len(o) and s[len(o)] in ":=|" :
            return s[len(o) + 1:].strip()
    return ""


def is_abstain(r, o):
    if ABSTAIN_RX.match(o.strip()):
        return True
    if r["meta"]["sampler"] == "S7":
        return bool(RESID_RX.search(def_line(r, o)))
    return False


def gold_index(r):
    return r["options"].index(r["gold"])


# visible metadata only (FIX RULES: G6 metadata = only what the model sees). Sidecar fields used are visible
# properties of the rendered row; label-derived or hidden fields (gold_kind, gold_pos, name_prior, yes_bad,
# polarity_tag, threshold, rel, twin_kind, rewrites, ecodes, u1, sel_*) are never used.
SIDE_CAT = ("ctype", "form", "layout", "mode", "world", "short", "fewshot_card", "inverted_card", "lookalike", "inert",
            "conseq_visible", "wkind", "neg")
SIDE_NUM = ("k", "k_all", "k_syn", "asked_pos", "n_terms_card")


def meta_feats(r, s=None):
    m = r["meta"]; s = s or {}; v = views(r)
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "domain_pack")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep"))
    cat["edge"] = ",".join(sorted(map(str, m.get("edge") or [])))
    cat["attack"] = str(bool(s.get("attack")))
    for k in SIDE_CAT:
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    num = {"len_state": float(len(r["state"])), "len_ins": float(len(r["instructions"])),
           "len_card": float(len(r.get("card") or "")), "n_lines_state": float(r["state"].count("\n")),
           "k_opts": float(len(r["options"]) if not is_yn(r) else 2),
           "n_omitted": float(len(s.get("omitted") or [])), "n_override": float(len(s.get("override_words") or []))}
    for k in SIDE_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
    nums = [float(x) for x in NUM_RX.findall(r["state"])][:30]
    num["state_n_numbers"] = float(len(nums)); num["state_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    if not is_yn(r):
        L = [len(o) for o in r["options"]]
        num["opt_len_mean"] = float(sum(L) / len(L)); num["opt_len_max"] = float(max(L))
    return cat, num


DEFLINE_RX = re.compile(r"^[\s>*•+\-|]*([«'\"\[]?[^:=|\n]{1,40}?[»'\"\]]?)\s*(?::|=|\|)\s+\S")


def card_terms(r):
    """ordered term/code names that start a definition line in the card-side text (card + instructions minus
    the question paragraph), visible parsing only; table header 'code' excluded."""
    txt = (r.get("card") or "") + "\n" + split_q(r["instructions"])[1]
    out = []
    for ln in txt.split("\n"):
        m = DEFLINE_RX.match(ln)
        if m:
            t = m.group(1).strip()
            if t and t.lower() not in ("code", "example", "q", "a", "answer", "answer key", "note") and len(t.split()) <= 4 and t not in out:
                out.append(t)
    return out


def asked_term(r, terms=None):
    terms = terms if terms is not None else card_terms(r)
    q = split_q(r["instructions"])[0]
    hits = [t for t in terms if re.search(r"(?<![\w«'\"\[])" + re.escape(t) + r"(?![\w»'\"\]])", q)]
    return max(hits, key=len) if hits else None
