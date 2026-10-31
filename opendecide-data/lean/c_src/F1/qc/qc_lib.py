"""Shared loaders for the independent F1 QC gates (G5-G18). Written by the F1 checker, not by the F1 generator author;
it imports nothing from c_src/F1/gen or c_src/F1/solverB. Prints counts only, never row text."""
import hashlib, json, math, random, re, string, sys
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F1 = LEAN / "c_src/F1"
OUT = F1 / "out"
QC = F1 / "qc"
TMP = F1 / "tmp/qc"
# sidecar fields that carry or derive from the label (never used as metadata features)
LABEL_FIELDS = {"id", "gold", "gold_source", "X_role", "yes_bad", "flips", "err_models", "group_id"}


def load(name):
    rows = [json.loads(l) for l in open(OUT / f"{name}.jsonl")]
    side = {}
    p = OUT / f"{name}.sidecar.jsonl"
    if p.exists():
        for l in open(p):
            s = json.loads(l); side[s["id"]] = s
    return rows, side


def load_rel(name):
    p = OUT / f"{name}.rel.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() else []


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


def gold_text(r):
    if is_yn(r):
        return "Yes" if r["gold"] == 1 else "No"
    g = r["gold"]
    return r["options"][g] if isinstance(g, int) else g  # choice gold is the option text


ABSTAIN_ROLES = {"cbd", "none"}
NUM_RX = re.compile(r"\d[\d,]*(?:\.\d+)?")


def split_q(ins):
    """Question paragraph = the last paragraph of `instructions` holding '?'; rest = the other paragraphs."""
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


SIDE_CAT = ("qtype", "world", "policy", "tie", "unit_kind", "twin_kind", "role", "label_form", "sampler", "short",
            "attack", "pol", "X_role", "deep")
SIDE_NUM = ("n_rules", "n_amend", "n_elements", "depth", "len_tokens", "k_syn", "k_all", "n_inert", "k")


def meta_feats(r, s):
    """Visible / structural metadata for G6(d), G7: row meta + sidecar fields that are not label-derived.
    Excluded: gold, gold_source, gold_role, gold_basis, yes_bad, flips, err_models, traps, position, A, boundary
    (solution-derived; their missingness encodes the gold source)."""
    m = r["meta"]; v = views(r); s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style")}
    cat["edge"] = ",".join(sorted(m.get("edge") or []))
    for k in SIDE_CAT:
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    num = {"len_state": len(r["state"]), "len_ins": len(r["instructions"]), "len_card": len(r.get("card") or ""),
           "n_lines_state": r["state"].count("\n"), "k_opts": len(v["opts"]) if not is_yn(r) else 2}
    for k in SIDE_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
    nums = [float(x.replace(",", "")) for x in NUM_RX.findall(v["q"])][:20]
    num["q_n_numbers"] = len(nums); num["q_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    roles = s.get("option_roles") or []
    for ro in ("default", "escalate", "fallback", "M", "cbd", "none", "case", "other"):
        num["n_role_" + ro] = float(sum(1 for x in roles if x == ro))
    if s.get("code_share") is not None:
        num["code_share"] = float(s["code_share"])
    return cat, num
