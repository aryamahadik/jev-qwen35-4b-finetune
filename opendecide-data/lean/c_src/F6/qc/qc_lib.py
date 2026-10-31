"""Shared loaders for the independent F6 QC gates (G5-G18). Written by the F6 checker, not by the F6 generator or
solver authors; it imports nothing from c_src/F6/gen or c_src/F6/solverB. Prints counts only, never row text."""
import json, math, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F6 = LEAN / "c_src/F6"
OUT = F6 / "out"
QC = F6 / "qc"
TMP = F6 / "tmp/qc"
TMP.mkdir(parents=True, exist_ok=True)
PROG = LEAN / "c_build/progress_phase2.log"
# side-file fields that carry or derive from the label: never metadata features
LABEL_FIELDS = {"id", "gold_class", "p_set", "t_set", "settle", "decidable", "decisive_gap", "loader", "spec", "g3",
                "cases", "valence", "switches_stated", "wording_text", "frames_card"}


def progress(msg):
    import time
    with open(PROG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [F6] checker: {msg}\n")


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / f"{name}.qc_side.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
    return rows, side


def load_rel(name):
    p = OUT / f"{name}.relations.jsonl"
    return [json.loads(l) for l in open(p) if l.strip()] if p.exists() else []


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


def split_q(ins):
    """Question = the last paragraph of `instructions` holding '?'; rest = every other paragraph."""
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def views(r):
    q, rest = split_q(r["instructions"])
    cardnoq = ((r.get("card") or "") + "\n\n" + rest).strip()
    return {"q": q, "cardnoq": cardnoq, "state": r["state"], "opts": list(r["options"] or [])}


def full_text(r):
    return "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


NUM_RX = re.compile(r"\d[\d,]*(?:\.\d+)?")
SIDE_CAT = ("kind", "form", "frame_id", "question_frame", "card_variant", "label_form", "attack", "qkind")
SIDE_NUM = ("n_gaps", "k", "tokens", "k_syn", "k_all", "k_syn_S", "k_all_S", "k_syn_frame", "k_all_frame")


def meta_feats(r, s):
    """Visible / structural metadata for G6(d) and G7: v4 G6(d) list (depth, rule count proxy, lengths, option
    lengths, number magnitudes, name pool = domain pack, template = format style / wording, sampler) plus the F6 G7
    list (gap kinds, n_gaps, gap positions, frame_id, label form). Label-derived side fields are excluded."""
    m = r["meta"]; v = views(r); s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style", "sampler", "domain_pack", "subtype")}
    cat["depth"] = str(m.get("depth")); cat["deep"] = str(m.get("deep"))
    for e in m.get("edge") or []:
        cat["edge:" + e] = "1"
    for k in SIDE_CAT:
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    for g in s.get("gap_kinds") or []:
        cat["gk:" + g] = "1"
    for p in s.get("gap_positions") or []:
        cat["gp:" + str(p)] = "1"
    num = {"len_state": len(r["state"]), "len_ins": len(r["instructions"]), "len_card": len(r.get("card") or ""),
           "n_lines_state": r["state"].count("\n"), "k_opts": len(v["opts"]) if not is_yn(r) else 2,
           "depth_n": float(m.get("depth") or 0)}
    if not is_yn(r):
        L = [len(o) for o in v["opts"]]
        num["opt_len_mean"] = sum(L) / len(L); num["opt_len_max"] = max(L); num["opt_len_min"] = min(L)
    for k in SIDE_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
    nums = [float(x.replace(",", "")) for x in NUM_RX.findall(v["q"])][:20]
    num["q_n_numbers"] = len(nums); num["q_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    sn = [float(x.replace(",", "")) for x in NUM_RX.findall(r["state"])][:200]
    num["state_n_numbers"] = len(sn); num["state_max_num_log"] = math.log1p(max(sn)) if sn else 0.0
    num["n_rules_proxy"] = float(len(re.findall(r"(?im)^\s*(?:[-*]\s*)?(?:rule\b|\d+[.)]\s)", full_text(r))))
    return cat, num
