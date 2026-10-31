"""Shared loaders and views for the independent F8 QC gates (G5-G18). Written by the F8 checker (never an F8 generator
or solver author); imports nothing from c_src/F8/gen or c_src/F8/solverB. Reads out/<name>.jsonl, its relations file
and the G0-sec-12 sidecar out/f8_controls_<name>.jsonl (the QC agent joins it on id for G6, G7, G10; G0 12).
G6/G7 metadata = only what the model can see in the prompt (F8 G0 10.3, "observable only"): sidecar fields that are
hidden values or label-derived (gold_answer, placement, d_steps, distractor_errors, flip_kind, edge_row,
evidence_changes, hl, gold_probs_exact, tier_step, unit_id, render_hash) and meta.edge / twin fields are never features.
Question view = the last paragraph of `instructions` holding '?' (else its last paragraph); card-without-question =
`card` + the other paragraphs of `instructions` (on choice rows the card block sits in `instructions`, G0 1)."""
import json, math, os, re, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F8 = LEAN / "c_src/F8"
OUT = F8 / "out"
QC = F8 / "qc"
TMP = F8 / "tmp/chk"
TMP.mkdir(parents=True, exist_ok=True)
NUM_RX = re.compile(r"(?<![A-Za-z0-9-])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9-])\d+(?:\.\d+)?")
ABSTAIN_RX = re.compile(r"^(none of (these|the listed.*)|not enough information.*|cannot be determined.*|"
                        r"can't be determined.*|undetermined.*|not determinable.*|insufficient.*|cannot tell.*|"
                        r"can not be determined.*|unknown.*|cannot say.*|not determinable.*)$", re.I)
HIDDEN_SIDE = ("gold_answer", "placement", "d_steps", "distractor_errors", "flip_kind", "edge_row", "evidence_changes",
               "hl", "gold_probs_exact", "tier_step", "unit_id", "render_hash", "id", "card_id")


def load(name):
    return [json.loads(l) for l in open(OUT / f"{name}.jsonl")]


def load_side(name):
    return {d["id"]: d for d in (json.loads(l) for l in open(OUT / f"f8_controls_{name}.jsonl"))}


def load_relations(name):
    p = OUT / f"relations_{name}.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() and p.stat().st_size else []


def is_yn(r):
    return r["qtype"] == "noul"


def split_q(ins):
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    if not paras:
        return "", ""
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def views(r):
    q, rest = split_q(r["instructions"])
    return {"q": q, "cardnoq": ((r.get("card") or "") + "\n\n" + rest).strip(), "state": r["state"],
            "opts": list(r["options"] or [])}


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


def gold_index(r):
    if is_yn(r):
        return None
    g = r["gold"]
    return g if isinstance(g, int) else r["options"].index(g)


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def roundness(x):
    if x != int(x):
        return -1
    x = int(x); k = 0
    while x and x % 10 == 0:
        x //= 10; k += 1
    return k


def meta_feats(r, s):
    """(categorical, numeric) observable features: C_DATA_SPEC 8 G6 (d) generic list + F8 G0 10.3 list."""
    m = r["meta"]; v = views(r); st = r["state"]; full = full_text(r).lower()
    cat = {k: str(m.get(k)) for k in ("sampler", "format_style", "wording_id", "defs_style", "domain_pack", "subtype")}
    cat.update({"deep": str(m.get("deep")), "qtype": r["qtype"]})
    for k in ("qform", "yn_kind", "comparator", "direction", "world", "card_version", "subset_class", "masked",
              "card_size", "yes_is_bad"):
        cat[k] = str(s.get(k))
    for rp in (s.get("representation") or []):
        cat["repr=" + str(rp)] = "1"
    t = s.get("t_repr") or {}
    cat["t_rep"] = str(t.get("rep")); cat["t_denom"] = str(t.get("denom"))
    num = {}
    for sid in set(s.get("sem_ids") or []):
        num["sem:" + sid] = 1.0
    qn = nums(v["q"]); sn = nums(st); T = max(qn) if qn else 0.0
    num.update({"depth": float(m.get("depth") or 0), "polarity": float(s.get("polarity") or 0),
                "k_syn": float(s.get("k_syn") or 0), "k_all": float(s.get("k_all") or 0),
                "n_unknown": float(s.get("n_unknown") or 0), "n_options": float(s.get("n_options") or 0),
                "ntok": float(s.get("ntok") or 0), "t_digits": float(t.get("digits") or 0),
                "t_trailing_zeros": float(t.get("trailing_zeros") or 0),
                "len_state": len(st), "len_ins": len(r["instructions"]), "len_card": len(r.get("card") or ""),
                "len_q": len(v["q"]), "n_lines_state": st.count("\n"),
                "n_lines_rules": r["instructions"].count("\n") + (r.get("card") or "").count("\n"),
                "unless": float("unless" in full), "override": float("override" in full),
                "only_if": float("only if" in full), "not_recorded": float(st.lower().count("not recorded")),
                "T_log": math.log1p(abs(T)), "T_round": float(roundness(T)) if qn else -2.0,
                "q_n_numbers": float(len(qn)), "n_stated": float(len(sn)),
                "largest_log": math.log1p(max(sn)) if sn else 0.0})
    opts = v["opts"]
    if opts and not is_yn(r):
        ls = [len(o) for o in opts]
        num.update({"opt_len_mean": float(sum(ls)) / len(ls), "opt_len_max": float(max(ls)),
                    "opt_len_min": float(min(ls)), "k_opts": float(len(opts))})
    return cat, num
