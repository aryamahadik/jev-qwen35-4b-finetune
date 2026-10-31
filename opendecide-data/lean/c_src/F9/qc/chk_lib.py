"""Shared loaders for the independent F9 QC checker (check:F9, c-lanes-v3). Imports nothing from c_src/F9/gen or
c_src/F9/solverB. Prints counts only, never row text.
Views follow G0 1.10 ("G6 / G7 inputs are taken from the row's parts before placement"): the question is the side
file's `qtext` (the visible question string; it occurs exactly once in `instructions` on every row); the card view is
`card` + `instructions` with the question removed (on choice rows every card element sits in `instructions`)."""
import hashlib, json, math, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F9 = LEAN / "c_src/F9"
OUT = F9 / "out"
QC = F9 / "qc"
TMP = F9 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)


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


ABSTAIN_RX = re.compile(r"^(none of these|cannot be determined|no such .+|two or more .+ tie)$")
NUM_RX = re.compile(r"-?\d+(?:[.,]\d+)?")


def abstain_kind(o):
    o = o.strip()
    if o == "none of these":
        return "none_of_these"
    if o == "cannot be determined":
        return "cbd"
    if o.startswith("no such "):
        return "no_record"
    if o.startswith("two or more ") and o.endswith(" tie"):
        return "tie"
    return None


def qtext(r, s):
    q = (s or {}).get("qtext")
    if q and r["instructions"].count(q) == 1:
        return q
    paras = [p for p in r["instructions"].strip().split("\n\n") if p.strip()]
    return next((p for p in reversed(paras) if "?" in p), paras[-1])


def views(r, s):
    q = qtext(r, s)
    rest = r["instructions"].replace(q, " ", 1)
    return {"q": q, "cardnoq": ((r.get("card") or "") + "\n\n" + rest).strip(), "state": r["state"],
            "opts": list(r["options"] or [])}


def as_num(o):
    t = o.strip().replace(",", "")
    m = re.fullmatch(r"[$€£¥]?\s?(-?\d+(?:\.\d+)?)(?:\s*[A-Za-z%°/][A-Za-z%°/ ]{0,19})?", t)
    return float(m.group(1)) if m else None


# Visible metadata only (FIX RULE "G6 metadata = only what the model sees"). Used: meta fields that describe the
# rendered row (format style, wording, definition style, sampler, pack, depth, subtype = question operator) and side
# fields that are visible properties of the rendered row (container, frame = question template, card mode, masked
# legend, inverted / few-shot card, attack text present, examples shown, negation counts of the question, size bin,
# token length). Never used (label-derived or hidden): edge, placement, decile, polarity_bad, plan, unit_kind,
# twin_kind, gold_payload, options_full, shown, struct, sem_stated, q, swapped (the swap is a definition reading).
SIDE_CAT = ("container", "frame", "mode", "masked", "inverted", "fewshot_card", "attack", "form")
SIDE_NUM = ("k_syn", "k_all", "n_examples", "bin", "real_tokens")


def meta_feats(r, s=None):
    m = r["meta"]; s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "domain_pack", "subtype")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep")); cat["role"] = str(r.get("role"))
    for k in SIDE_CAT:
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    num = {"len_state": float(len(r["state"])), "len_ins": float(len(r["instructions"])),
           "len_card": float(len(r.get("card") or "")), "n_lines_state": float(r["state"].count("\n")),
           "k_opts": float(len(r["options"]) if not is_yn(r) else 2)}
    for k in SIDE_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
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


def set_ids(o):
    """record-set option '<a> and <b> only' -> frozenset of ids; None if not a set option."""
    if not o.endswith(" only"):
        return None
    body = o[:-5]
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", body)
    return frozenset(p.strip() for p in parts if p.strip())
