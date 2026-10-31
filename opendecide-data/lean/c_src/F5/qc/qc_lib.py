"""Shared loaders and views for the independent F5 QC gates (G5-G18). Written by the F5 checker (never an F5 generator
or solver author); imports nothing from c_src/F5/gen or solverB. Reads out/<name>.jsonl, its relations file and the
G0-sec-9 QC sidecar out/<name>.F5_polarity.jsonl (allow-listed for G6, G7, G10). Label-derived sidecar fields
(gold, v_P, pair_change) are never features."""
import json, os, re, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F5 = LEAN / "c_src/F5"
OUT = F5 / "out"
QC = F5 / "qc"
TMP = F5 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
LABEL_SIDE = ("gold", "v_P", "pair_change", "id", "base_id", "card_id", "pair_id", "lf", "p_clause")
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9-])\d+(?:\.\d+)?")
SENT_RX = re.compile(r"(?<=[.!?])\s+")
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def load(name):
    return [json.loads(l) for l in open(OUT / f"{name}.jsonl")]


def load_side(name):
    return {d["id"]: d for d in (json.loads(l) for l in open(OUT / f"{name}.F5_polarity.jsonl"))}


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


def split_q(ins):
    """question = sentence(s) of instructions carrying '?'; rest = the wording around it."""
    qs, rest = [], []
    for line in ins.strip().split("\n"):
        for s in SENT_RX.split(line):
            (qs if "?" in s else rest).append(s)
    return " ".join(qs).strip(), " ".join(rest).strip()


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
