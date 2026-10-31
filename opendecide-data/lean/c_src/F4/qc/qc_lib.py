"""Shared loaders and views for the independent F4 QC gates (G5, G6, G7, G8, G10-G12, G15, G18).
Written by the F4 checker (never an F4 generator / solver author); imports nothing from c_src/F4/gen or solverB.
Views follow C_DATA_SPEC 8 G6: question = sentence(s) of `instructions` carrying '?'; card-without-question = `card`
+ the rest of `instructions`; options; metadata = row meta + edge tags (label-derived tags excluded) + text numbers."""
import json, math, os, re, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F4 = LEAN / "c_src/F4"
OUT = F4 / "out"
QC = F4 / "qc"
TMP = F4 / "tmp/checker"
TMP.mkdir(parents=True, exist_ok=True)
# edge-tag prefixes that are label-derived by construction (excluded from G6 (d) / G7 metadata features)
LABEL_TAGS = ("L", "pivot")
ABSTAIN_RX = re.compile(r"^(none of (these|the).*|not enough information.*|cannot be determined.*|undetermined.*|"
                        r"insufficient.*|cannot tell.*)$", re.I)
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9-])\d+(?:\.\d+)?")
SENT_RX = re.compile(r"(?<=[.!?])\s+")


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
        if len(decoder_io.WIDE) < 100:  # placeholder two-letter labels (as fmt1 _serving); a Readout fills the real set
            import string
            U = string.ascii_uppercase
            decoder_io.WIDE = list(U) + [a + b for a in U for b in U]
        _DIO = decoder_io
    return _DIO


def model_view(r, perm=None):
    return dio().user_msg(r, perm)


def gold_letter(r):
    d = dio()
    if r["qtype"] == "noul":
        return "A" if r["gold"] == 1 else "B"
    return d.label(r["options"].index(r["gold"]))


def is_yn(r):
    return r["qtype"] == "noul"


def split_q(ins):
    qs, rest = [], []
    for line in ins.strip().split("\n"):
        for s in SENT_RX.split(line):
            (qs if "?" in s else rest).append(s)
        rest.append("\n")
    return " ".join(qs).strip(), " ".join(rest).strip()


def views(r):
    q, rest = split_q(r["instructions"])
    cardnoq = ((r.get("card") or "") + "\n\n" + rest).strip()
    return {"q": q, "cardnoq": cardnoq, "state": r["state"], "opts": list(r["options"] or [])}


def full_text(r):
    return "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])


def is_abstain(o):
    return bool(ABSTAIN_RX.match(o.strip()))


def nums(text):
    out = []
    for x in NUM_RX.findall(text):
        try:
            out.append(float(x.replace(",", "")))
        except ValueError:
            pass
    return out


def tags(r):
    return [e for e in r["meta"].get("edge", []) if e.split(":")[0] not in LABEL_TAGS]


def yes_label(r):
    """1 = gold yes, 0 = gold no, None for choice rows."""
    return int(r["gold"]) if r["qtype"] == "noul" else None
