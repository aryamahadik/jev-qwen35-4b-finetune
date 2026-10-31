"""Shared loaders and views for the independent F2 QC gates (G6, G7, G8, G10-G12, G15, G18). Written by the F2 checker,
not by the F2 generator author; imports nothing from c_src/F2/gen or c_src/F2/solverB. Views follow C_DATA_SPEC 8 and
F2 G0 sections 3.8 and 6: question = the sentence(s) of `instructions` that carry '?'; card-without-question = `card`
+ the rest of `instructions`; options; metadata = row meta + edge tags (label-derived tags excluded) + text numbers."""
import json, math, re
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F2 = LEAN / "c_src/F2"
OUT = F2 / "out"
QC = F2 / "qc"
# edge tags that are label-derived or label-adjacent by construction (not text properties): excluded from (d) / G7
LABEL_TAGS = ("boundary", "dec", "bind", "nei", "err", "tie")
ABSTAIN_RX = re.compile(r"^(none of (these|the listed.*)|not enough information.*|cannot be determined.*|"
                        r"undetermined.*|not determinable.*|no record.*|insufficient.*|cannot tell.*)$", re.I)
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9-])\d+(?:\.\d+)?")
SENT_RX = re.compile(r"(?<=[.!?])\s+")


def load(name):
    return [json.loads(l) for l in open(OUT / f"{name}.jsonl")]


def load_relations(name):
    p = OUT / f"{name}.relations.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() else []


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
    return [e for e in r["meta"]["edge"] if e.split(":")[0] not in LABEL_TAGS]


CUR_RX = re.compile(r"\b(EUR|USD|GBP|CHF|JPY|AUD|CAD|NZD|SEK|NOK|DKK|INR|ZAR|SGD|credits?|tokens?|points?)\b|[$£€¥]")
SINGLE = ("cmp", "cue", "syn", "tf", "var", "world", "money", "b1", "named", "mech", "pol", "sel", "ops", "abst", "cases")


def roundness(x):
    if x != int(x):
        return -1
    x = int(x); k = 0
    while x and x % 10 == 0:
        x //= 10; k += 1
    return k


def meta_feats(r):
    """(categorical dict, numeric dict) per C_DATA_SPEC 8 G6 (d) and F2 G0 6; never a label field or label tag."""
    m = r["meta"]; v = views(r); tg = tags(r)
    cat = {k: str(m.get(k)) for k in ("sampler", "format_style", "wording_id", "defs_style", "domain_pack")}
    cat["deep"] = str(m.get("deep")); cat["qtype"] = r["qtype"]
    for p in SINGLE:
        vals = [e for e in tg if e.split(":")[0] == p]
        cat["t_" + p] = vals[0] if vals else "none"
    num = {}
    for e in tg:
        p = e.split(":")[0]
        if p in ("has", "sem") or ":" not in e:
            num["f_" + e] = 1.0
    st = r["state"]; opts = v["opts"]
    num.update({"depth": float(m.get("depth") or 0), "len_state": len(st), "len_ins": len(r["instructions"]),
                "len_card": len(r.get("card") or ""), "len_q": len(v["q"]),
                "n_rule_lines": r["instructions"].count("\n") + (r.get("card") or "").count("\n"),
                "k_opts": float(len(opts)) if opts else 2.0, "not_recorded": float("not recorded" in st.lower()),
                "n_not_recorded": float(st.lower().count("not recorded")), "tokens": float(m.get("tokens") or 0)})
    if opts:
        ls = [len(o) for o in opts]
        num.update({"opt_len_mean": float(sum(ls)) / len(ls), "opt_len_max": float(max(ls)), "opt_len_min": float(min(ls))})
    qn = nums(v["q"]); sn = nums(st)
    T = max(qn) if qn else 0.0
    num.update({"T_log": math.log1p(T), "T_round": float(roundness(T)) if qn else -2.0, "q_n_numbers": float(len(qn)),
                "n_stated": float(len(sn)), "largest_log": math.log1p(max(sn)) if sn else 0.0,
                "sum_log": math.log1p(sum(sn)) if sn else 0.0,
                "sign_T_largest": float((T > max(sn)) - (T < max(sn))) if (qn and sn) else 0.0,
                "sign_T_sum": float((T > sum(sn)) - (T < sum(sn))) if (qn and sn) else 0.0,
                "T_dec": float(any(x != int(x) for x in qn))})
    cur = CUR_RX.findall(st)
    cat["currency"] = (cur[0] if isinstance(cur[0], str) else "") if cur else "none"
    return cat, num


import datetime as _dt
_DATE_FMTS = ("%d %B %Y", "%B %d, %Y", "%Y-%m-%d", "%A, %d %B %Y", "%A, %B %d, %Y")
_VAL_RX = re.compile(r"^\s*(\d[\d,]*(?:\.\d+)?)\s+[A-Za-z]")


def opt_value(o):
    """Order key of an option: ('date', ordinal) | ('num', value) | None (bands, names, IDs, abstain)."""
    s = o.strip()
    for f in _DATE_FMTS:
        try:
            return ("date", _dt.datetime.strptime(s, f).toordinal())
        except ValueError:
            pass
    m = _VAL_RX.match(s)
    if m:
        return ("num", float(m.group(1).replace(",", "")))
    return None


def opt_rank_kinds(r):
    """Per option: set of rank kinds over the row's ordered options (value/date options, else first-mention order of
    the option names in instructions + state, which is the band / outcome listing order)."""
    opts = r["options"]; vals = [opt_value(o) for o in opts]
    idx = [i for i, o in enumerate(opts) if not is_abstain(o)]
    keys = {}
    if idx and all(vals[i] is not None for i in idx) and len({vals[i][0] for i in idx}) == 1:
        keys = {i: vals[i][1] for i in idx}; mode = "val"
    else:
        txt = r["instructions"] + "\n" + r["state"]
        pos = {i: txt.find(opts[i]) for i in idx}
        if idx and all(p >= 0 for p in pos.values()):
            keys = pos; mode = "list"
        else:
            return [set() for _ in opts], None
    uk = sorted(set(keys.values()))
    out = []
    for i in range(len(opts)):
        k = set()
        if i in keys and len(uk) >= 2:
            if keys[i] == uk[0]: k.add(f"rank:{mode}_first")
            if keys[i] == uk[-1]: k.add(f"rank:{mode}_last")
            if len(uk) >= 3 and keys[i] not in (uk[0], uk[-1]): k.add(f"rank:{mode}_inner")
        out.append(k)
    return out, mode
