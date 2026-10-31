"""SEM line sets per card version (G0 spec 3.1 rendering rules) and the convention-invariance lint (CI lint).

sem_set(card, version) -> ordered SEM keys the version renders (keys of lexicon.SEM, e.g. 'SEM-01', 'SEM-02sum').
ci_edges(S, card, version) -> (edge ids, missing ids): every SEM id whose alternative reading changes the row's label
or abstain decision; 'missing' are those not rendered in the row's version (the row must then be redrawn).
"""
from __future__ import annotations

from solver_a import CV, Undetermined, solve

ORDER = ["SEM-01", "SEM-01a", "SEM-01b", "SEM-02", "SEM-02sum", "SEM-02grp", "SEM-02ch", "SEM-02yn", "SEM-03",
         "SEM-28", "SEM-06", "SEM-10", "SEM-13", "SEM-23", "SEM-07", "SEM-04", "SEM-14", "SEM-05", "SEM-15",
         "SEM-16", "SEM-18", "SEM-17", "SEM-29", "SEM-30", "SEM-26", "SEM-27", "SEM-11lo", "SEM-11hi",
         "SEM-20loss", "SEM-20net", "SEM-19", "SEM-21", "SEM-33", "SEM-22", "SEM-12", "SEM-24", "SEM-25",
         "SEM-31", "SEM-32c", "SEM-32o"]


def base_id(key: str) -> str:
    return key[:6]


def _features(card: dict) -> dict:
    r = card["rules"]
    sch, sub = card["schema"], card["sub"]
    q = card.get("q", {})
    conns = set()
    unless = False
    for ln in (r.get("scorecard") or {}).get("lines", []):
        conns.add(ln["cond"]["conn"])
        if ln.get("unless"):
            unless = True
            conns.add(ln["unless"]["conn"])
    for c in list((r.get("arules") or {}).values()) + list((r.get("only_if") or {}).values()) + \
            [o["cond"] for o in r.get("overrides") or []]:
        conns.add(c["conn"])
    outcome_model = sub == "expected" or q.get("def") == "el" or (sch == "mat" and r["mat"]["impact"] == "expected")
    amounts = outcome_model or sch in ("mat", "dec") or any(
        p["t"] == "amt" for ln in (r.get("scorecard") or {}).get("lines", []) for p in ln["cond"]["parts"])
    return {"conns": conns, "unless": unless, "outcome_model": outcome_model, "amounts": amounts,
            "risk": q.get("k") == "risk", "net": card.get("mode") == "net", "tec": q.get("k") == "tec",
            "en": q.get("k") == "en", "bayes": sub == "bayes", "joint": "joint" in (card.get("data_forms") or []),
            "ain": bool({"ain", "aoutof"} & set(card.get("reps") or [])), "open": card.get("open_rate", 0) > 0,
            "arules": bool(r.get("arules")), "scorecard": bool(r.get("scorecard"))}


def sem_set(card: dict, version: str) -> list:
    sch = card["schema"]
    f = _features(card)
    fi = card["flip_incl"]
    full = version == "full"
    s = []
    # always lines
    if full:
        s.append("SEM-01")
        if f["outcome_model"]:
            s.append("SEM-01b")
    if f["open"] and full:
        s += ["SEM-02", "SEM-03"]
        if f["outcome_model"]:
            s.append("SEM-02sum")
        if f["bayes"]:
            s.append("SEM-02grp")
        s.append("SEM-02yn" if sch == "yn" else "SEM-02ch")
    if sch in ("yn", "bin", "inv"):
        s += ["SEM-06", "SEM-10"]
    if f["amounts"]:
        s.append("SEM-13")
    if (f["tec"] or sch == "dec") and "SEM-03" not in s:
        s.append("SEM-03")                     # own costs may read 'None' or '0'

    if f["ain"]:
        s.append("SEM-23")
    if f["bayes"]:
        s += ["SEM-17", "SEM-30"]
        if f["joint"]:
            s.append("SEM-29")
        if full and fi["SEM-18"]:
            s.append("SEM-18")
    if sch == "pred":
        s.append("SEM-27")
    if card.get("two_signs"):
        s.append("SEM-26")
    if f["outcome_model"]:
        s.append("SEM-19")
    if f["net"]:
        s.append("SEM-20net")
    if sch == "dec":
        s += ["SEM-21", "SEM-33"]
    if f["risk"]:
        s.append("SEM-22")
    if sch in ("rank_top", "dec"):
        s.append("SEM-12")
    if sch == "mat":
        s.append("SEM-25")
    if f["arules"]:
        s.append("SEM-31")
    if sch == "inv":
        s.append("SEM-32c")
        if f["open"]:
            s.append("SEM-32o")
    if sch == "tier":
        s += ["SEM-05", "SEM-15"]
    if sch == "bin" and full:
        s.append("SEM-11" + card["rules"]["bin_conv"])
    if full and fi["SEM-28"]:
        s.append("SEM-28")
    # when-it-flips lines (full version only, drawn per card)
    if full:
        if f["conns"] & {"or", "xor1"} and fi["SEM-07"]:
            s.append("SEM-07")
        if f["unless"] and fi["SEM-04"]:
            s.append("SEM-04")
        if f["scorecard"] and fi["SEM-14"]:
            s.append("SEM-14")
        if sch == "tier" and fi["SEM-16"]:
            s.append("SEM-16")
        if f["outcome_model"] and not f["net"] and fi["SEM-20"]:
            s.append("SEM-20loss")
        if f["tec"] and sch != "dec" and fi["SEM-21"]:
            s.append("SEM-21")
        if f["en"] and fi["SEM-24"]:
            s.append("SEM-24")
    out = [k for k in ORDER if k in s]
    return out


# ------------------------------------------------------------------------------------------------ CI lint
def alternatives(S: dict) -> dict:
    """SEM id -> list of cv dicts, restricted to the alternatives that can apply to this row."""
    sub, form = S["sub"], S["form"]
    R = S["rules"]
    alts = {}
    has_sc = bool(R.get("scorecard")) or bool(R.get("arules"))
    if S["world"] != "open":
        alts["SEM-01"] = [CV(unstated="unknown"), CV(sem01_named=True)]
        if any(e.get("outs") for e in S["ents"]):
            alts["SEM-01"].append(CV(remainder="rescale"))
    else:
        alts["SEM-02"] = [CV(nr_zero=True), CV(abstain_any=True), CV(range_open=True), CV(groups_sum=True)]
    if form in ("yn_thr", "yn_act", "bin", "inv"):
        alts["SEM-06"] = [CV(cmp="swap", cmp_class=c) for c in ("thr", "amt", "q", "inv")]
        if S["world"] == "open":
            alts["SEM-06"].append(CV(range_open=True))
    if has_sc or R.get("only_if") or R.get("overrides"):
        alts["SEM-07"] = [CV(**{"or": "xor"}), CV(**{"or": "parity"}), CV(xor1="inclusive"), CV(xor1="atmost1"),
                          CV(xor1="parity")]
        alts["SEM-06"] = alts.get("SEM-06", []) + [CV(cmp="swap", cmp_class="amt")]
    if R.get("scorecard"):
        alts["SEM-04"] = [CV(unless="ignore"), CV(unless="iff")]
        alts["SEM-14"] = [CV(or_count="per_part"), CV(clamp="none"), CV(clamp="running")]
    if form == "tier":
        alts["SEM-05"] = [CV(only_if=x) for x in ("ignore", "sufficient", "limits_override", "one_down",
                                                  "skip_to_no_limit", "bottom")] + [CV(tier_by_name=True)]
        alts["SEM-15"] = [CV(override=x) for x in ("ignore", "lowest", "first")] + [CV(tier_by_name=True)]
        alts["SEM-16"] = [CV(cut_edge="lower")]
    if form == "bin":
        alts["SEM-11"] = [CV(bin_edge="other")]
    if sub == "bayes":
        forms = {e["bay"]["form"] for e in S["ents"] if e.get("bay")}
        alts["SEM-17"] = [CV(post="inverse"), CV(post="neglect"), CV(post="joint")]
        alts["SEM-30"] = [CV(post="prior")] if "joint" not in forms else []
        if "joint" in forms:
            alts["SEM-29"] = [CV(post="joint_as_cond")]
    if form == "pred":
        alts["SEM-27"] = [CV(post="prior"), CV(post="inverse")]
    if any(e.get("outs") for e in S["ents"]):
        alts["SEM-19"] = [CV(remainder="rescale")]
        alts["SEM-20"] = [CV(net="flip")] if S.get("mode") == "net" else [CV(el_max=True)]
    if any(e.get("cost") is not None for e in S["ents"]):
        alts["SEM-21"] = [CV(own_cost=x) for x in ("exclude", "twice", "on_event")]
    if S["q"].get("k") == "risk":
        alts["SEM-22"] = [CV(risk=x) for x in ("chance", "amount", "el") if x != S["q"]["def"]]
    if form in ("rank_top", "dec"):
        alts["SEM-12"] = [CV(tie=x) for x in ("first", "last", "higher_id", "none")]
    if S["q"].get("k") == "en":
        alts["SEM-24"] = [CV(en="at_least_one")]
    if form == "mat":
        alts["SEM-25"] = [CV(lvl_edge="other"), CV(grid="transposed"),
                          CV(impact="expected" if R["mat"]["impact"] == "loss" else "amount")]
    if form == "inv" and S["world"] == "open":
        alts["SEM-32"] = [CV(inv_open="closed_variant"), CV(inv_open="only_not_failing"),
                          CV(inv_open="sure_despite_und")]
    if form == "dec":
        alts["SEM-33"] = [CV(rank_by="amount"), CV(rank_by="chance")]
    return alts


def _res(S, cv):
    try:
        r = solve(S, cv)
        return (repr(r["ans"]), r["det"])
    except (Undetermined, ValueError, ZeroDivisionError, KeyError, IndexError):
        return ("UNDEF", False)


def ci_edges(S: dict, version_sems: list, base: tuple | None = None) -> tuple:
    """(edge ids sorted, missing ids sorted). base = solver A's (answer repr, det) under the standard reading."""
    base = base or _res(S, CV())
    rendered = {base_id(k) for k in version_sems}
    edges, missing = set(), set()
    for sid, cvs in alternatives(S).items():
        for cv in cvs:
            if _res(S, cv) != base:
                edges.add(sid)
                if sid not in rendered:
                    missing.add(sid)
                break
    return sorted(edges), sorted(missing)
