"""Shared loaders and views for the independent F3 QC gates (G6, G7, G8, G10-G12). Written by the F3 checker, not by
the F3 generator author; it imports nothing from c_src/F3/gen. Views follow spec 8 and F3 G0 section 1:
question = the question paragraph of `instructions` (the last paragraph holding '?'); card-without-question = `card`
+ `instructions` with the question paragraph removed; options; metadata = row meta + QC sidecar (label fields and the
card's drawn yes rate excluded)."""
import hashlib, json, math, re
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F3 = LEAN / "c_src/F3"
OUT = F3 / "out"
QC = F3 / "qc"
LABEL_FIELDS = {"yes", "gold_letter", "gold_is_abstain", "card_yes_rate", "id", "leak_key", "polarity_source"}
ABSTAIN_RX = re.compile(r"^(none of (these|the listed.*)|not enough information.*|cannot be determined.*|undetermined.*|not determinable.*|no record.*)$", re.I)
ID_RX = re.compile(r"\b[A-Z]{1,4}-[A-Z0-9]{2,6}\b")
NUM_RX = re.compile(r"\d+(?:[.,]\d+)?")


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / f"{name}.sidecar.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
    return rows, side


def load_relations(name):
    p = OUT / f"{name}.relations.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() else []


def is_yn(r):
    return r["qtype"] == "noul"


def split_q(ins):
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def views(r):
    q, rest = split_q(r["instructions"])
    cardnoq = ((r.get("card") or "") + "\n\n" + rest).strip()
    return {"q": q, "cardnoq": cardnoq, "state": r["state"], "opts": list(r["options"] or [])}


def full_text(r):
    return "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])


def is_abstain(o):
    return bool(ABSTAIN_RX.match(o.strip()))


def meta_feats(r, s):
    """Categorical + numeric metadata (spec 8 G6 (d) list + F3 G0 sidecar fields), never a label field."""
    m = r["meta"]; v = views(r)
    # twin_kind / twin_of are construction fields (a contrast twin exists only when the label flips), not in the spec
    # G6 (d) list; they are left out. decisive_decile is undefined (None) on rows with no decisive event (NEI and
    # some Q7 golds), so None is replaced by a seeded random decile instead of exposing a label-derived missingness.
    cat = {k: str(m.get(k)) for k in ("sampler", "format_style", "wording_id", "defs_style", "domain_pack")}
    cat["deep"] = str(m.get("deep")); cat["edge"] = ",".join(sorted(m.get("edge") or []))
    num = {"depth": m.get("depth") or 0, "len_state": len(r["state"]), "len_ins": len(r["instructions"]),
           "len_card": len(r.get("card") or ""), "n_rule_lines": r["instructions"].count("\n") + (r.get("card") or "").count("\n"),
           "k_opts": len(v["opts"]) if not is_yn(r) else 2}
    nums = [float(x.replace(",", "")) for x in NUM_RX.findall(v["q"])][:20]
    num["q_n_numbers"] = len(nums); num["q_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    ids = set(ID_RX.findall(r["state"])); num["state_n_ids"] = len(ids)
    num["q_n_ids"] = len(set(ID_RX.findall(v["q"])))
    for k, val in (s or {}).items():
        if k in LABEL_FIELDS:
            continue
        if k == "decisive_decile" and val is None:  # random decile (seeded by row id): no label-derived missingness
            val = int(hashlib.sha256(("dec:" + r["id"]).encode()).hexdigest()[:8], 16) % 10
        if isinstance(val, bool) or val is None or isinstance(val, str):
            cat["sc_" + k] = str(val)
        elif isinstance(val, (int, float)):
            num["sc_" + k] = float(val)
        elif isinstance(val, list):
            for x in val:
                num[f"sc_{k}={x}"] = 1.0
            num[f"sc_{k}_n"] = float(len(val))
    return cat, num
