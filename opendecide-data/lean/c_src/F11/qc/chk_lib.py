"""Shared loaders and views for the independent F11 QC gates (G5-G18). Written by the F11 checker (check:F11,
c-lanes-v3; never an F11 generator or solver author). Imports nothing from c_src/F11/gen or c_src/F11/solverB.
Reads out/<name>.jsonl and its relations file only."""
import json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F11 = LEAN / "c_src/F11"
OUT = F11 / "out"
QC = F11 / "qc"
TMP = F11 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d+(?:\.\d+)?")


def load(name):
    return [json.loads(l) for l in open(OUT / f"{name}.jsonl")]


def load_relations(name):
    p = OUT / f"{name}.relations.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() and p.stat().st_size else []


_DIO = None


def dio():
    global _DIO
    if _DIO is None:
        os.environ["OD_STYLE"] = "cygnet"
        sys.path.insert(0, str(LEAN))
        import decoder_io
        decoder_io.STYLE = "cygnet"
        decoder_io.LAYOUT = "schema_branch_mark"
        _DIO = decoder_io
    return _DIO


def model_view(r, perm=None):
    return dio().user_msg(r, perm)


def K(r):
    return len(r["options"]) if r["qtype"] == "choice" else 2


def label(r):
    """gold class index: choice -> option index; noul -> int gold (1 = yes)."""
    g = r["gold"]
    if r["qtype"] == "choice" and isinstance(g, str):
        return r["options"].index(g)
    return int(g)


def toks(text):
    return TOK.findall((text or "").lower())


def ngrams(text):
    t = toks(text)
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def nums(text):
    out = []
    for x in NUM_RX.findall(text or ""):
        try:
            out.append(float(x))
        except ValueError:
            pass
    return out


def sha256(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


_TOKZ = None


def tokenizer():
    global _TOKZ
    if _TOKZ is None:
        from transformers import AutoTokenizer
        _TOKZ = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
        dio().Readout(_TOKZ)  # fills decoder_io.WIDE (two-letter labels for options 27+), as at train/read time
    return _TOKZ


# ---------------------------------------------------------------- gate helpers (G6, G7, G10-G15); visible text only
SENT_RX = re.compile(r"(?<=[.!?])\s+")
ABSTAIN_RX = re.compile(r"(?i)^(none of (the|these)\b|not enough|cannot be determined|insufficient)")
MARK_RX = re.compile(r"\[([a-z][a-z \-]{1,30})\]\s*$")
NONCODE_LINE = re.compile(r"(?i)^\W*(example of|answer key|item \d|re:|unit:|file:|ref:)")


def is_yn(r):
    return r["qtype"] == "noul"


def gold_index(r):
    g = r["gold"]
    return r["options"].index(g) if isinstance(g, str) else int(g)


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def is_abstain(o):
    return bool(ABSTAIN_RX.match(o.strip()))


def split_q_para(ins):
    """question = last paragraph of `instructions` holding '?' (as the shared G8 tool's 'para' split); rest = others."""
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def q_sentence(ins):
    """the question sentence(s): every sentence of `instructions` holding '?'."""
    out = []
    for line in ins.split("\n"):
        out += [s for s in SENT_RX.split(line) if "?" in s]
    return " ".join(out).strip()


def views(r):
    qp, rest = split_q_para(r["instructions"])
    card = ((r.get("card") or "") + "\n\n" + rest).strip()
    return {"q": qp, "qsent": q_sentence(r["instructions"]), "cardnoq": card, "state": r["state"]}


def full_text(r):
    return "\n".join([r.get("card") or "", r["instructions"], r["state"]] + list(r.get("options") or []))


def wb_find(text, o):
    """first whole-word occurrence of o in text, or -1."""
    m = re.search(r"(?<![A-Za-z0-9])" + re.escape(o) + r"(?![A-Za-z0-9])", text)
    return m.start() if m else -1


def card_lines(r):
    """card lines that can list codes (bullets / table rows / key lines), worked-item and example lines dropped."""
    v = views(r)["cardnoq"]
    out = []
    for ln in v.split("\n"):
        s = ln.strip().lstrip("-*•>|#0123456789. ").strip()
        if s and not NONCODE_LINE.match(s):
            out.append(s)
    return out


def option_card_line(r, o, lines=None):
    """index and text of the first card line where option o occurs as a whole word (the card list position)."""
    lines = card_lines(r) if lines is None else lines
    for i, s in enumerate(lines):
        if wb_find(s, o) >= 0:
            return i, s
    return -1, ""


def meta_feats(r):
    """(categorical, numeric) observable features (C_DATA_SPEC 8 G6 (d) + F11 G0 6 list; only what the model sees)."""
    m = r["meta"]; v = views(r); st = r["state"]; e = set(m.get("edge") or [])
    cat = {k: str(m.get(k)) for k in ("sampler", "format_style", "wording_id", "defs_style", "domain_pack", "subtype")}
    cat.update({"deep": str(m.get("deep")), "depth": str(m.get("depth")), "short_card": str("short_card" in e),
                "masked": str("masked" in e), "swapped": str("swapped" in e), "has_card_field": str(bool(r.get("card"))),
                "examples": str("Example of" in v["cardnoq"]), "worked": str("Answer key" in v["cardnoq"])})
    ns = nums(st); lines = card_lines(r)
    num = {"len_card_log": round(math.log2(1 + len(v["cardnoq"])), 1), "len_state_log": round(math.log2(1 + len(st)), 1),
           "len_q": float(len(v["q"])), "n_sent_state": float(len(SENT_RX.split(st))), "n_nums_state": float(len(ns)),
           "num_max_log": round(math.log2(1 + max([abs(x) for x in ns] or [0])), 1), "n_card_lines": float(len(lines)),
           "n_marks": float(sum(1 for s in lines if MARK_RX.search(s))), "n_nl_state": float(st.count("\n"))}
    if r.get("options"):
        ls = [len(o) for o in r["options"]]
        num.update({"k": float(len(ls)), "opt_len_min": float(min(ls)), "opt_len_max": float(max(ls)),
                    "opt_len_mean": round(sum(ls) / len(ls), 1)})
    return cat, num


import math  # noqa: E402
