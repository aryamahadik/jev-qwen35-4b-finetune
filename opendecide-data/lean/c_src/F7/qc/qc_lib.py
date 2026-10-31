"""Shared loaders and views for the independent F7 QC gates (G5-G18). Written by the F7 checker (never an F7 generator
or solver author); imports nothing from c_src/F7/gen or c_src/F7/solverB. Reads out/<name>.jsonl and its relations
file only. Label-derived meta (edge alt_level / placement, case_features, row_kind, twin_kind) is never a G6 feature."""
import json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F7 = LEAN / "c_src/F7"
OUT = F7 / "out"
QC = F7 / "qc"
TMP = F7 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9-])\d+(?:\.\d+)?")
SENT_RX = re.compile(r"(?<=[.!?])\s+")
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
NEG_RX = re.compile(r"\b(no|not|never|none|absent|missing|false|n|without|lacks?|unknown|blank)\b", re.I)


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


def level(r):
    """gold level index 0..K-1 (option_level of the gold option text)."""
    return int(r["meta"]["option_level"][r["gold"]])


def K(r):
    return len(r["options"])


def paras(ins):
    return [p for p in re.split(r"\n\s*\n", ins.strip()) if p.strip()]


def card_paras(rows):
    """card_id -> set of instruction paragraphs present on >= 50% of the card's rows (= card content: C-lines, rubric,
    worked cases). Everything else in `instructions` (wording, question, entity line) is row-level."""
    cnt, n = defaultdict(Counter), Counter()
    for r in rows:
        c = r["meta"]["card_id"]; n[c] += 1
        cnt[c].update(set(paras(r["instructions"])))
    return {c: {p for p, k in cnt[c].items() if k >= 0.5 * n[c]} for c in cnt}


def split_ins(r, cp):
    """-> (card content in instructions, row-level wording + question)."""
    keep = cp[r["meta"]["card_id"]]
    ps = paras(r["instructions"])
    return "\n\n".join(p for p in ps if p in keep), "\n\n".join(p for p in ps if p not in keep)


def full_text(r):
    return "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])


def nums(text):
    out = []
    for x in NUM_RX.findall(text):
        try:
            out.append(float(x.replace(",", "")))
        except ValueError:
            pass
    return out


def toks(text):
    return TOK.findall(text.lower())


def ngrams(text):
    t = toks(text)
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def opt_name(o):
    """'Level 3 - Elevated' -> 'Elevated' (the level name after the number)."""
    m = re.match(r"^\s*\S+\s+\d+\s*-\s*(.+)$", o)
    return m.group(1).strip() if m else o


def opt_num(o):
    m = re.match(r"^\s*\S+\s+(\d+)", o)
    return m.group(1) if m else None


def card_defs(card):
    out = {}
    for line in (card or "").splitlines():
        if line.startswith("- ") and ": " in line:
            k, v = line[2:].split(": ", 1)
            out[k] = v
    return out
