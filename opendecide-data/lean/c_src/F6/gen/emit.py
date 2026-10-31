"""Row emission: a row record (structure + form + targets) -> the 2.4 row (rendered by fmt1, loader-checked) and its
QC side record. Dispatches on the structure kind (rules / table / timeline)."""
from __future__ import annotations

from . import common  # noqa: F401  (sys.path for fmt1)

import random

from fmt1 import pool as fpool
from fmt1.render import FormatError

from .common import rng_for, unit, h64
from . import rowmake as M, render_f6 as RF, rules_card as RC, rules_rows as RR, styles_f6 as ST, rules_gen as G
from . import solver_a as A
from .lex import sw

YN = ("qdet", "qest", "qplain")


def gloss_entries(card: dict, names: list[str], what: str, seed) -> list[dict]:
    pk = card["pack"]
    rng = random.Random(seed)
    role = card["P"]["case_noun"] if not pk.get("role") else pk["role"]
    doc = (pk.get("docs") or ["case file"])[0]
    if what == "out":
        tpl = ["a result entered on the file", "a decision noted on the file", "a recorded result"]
    else:
        tpl = [f"an entry the {role} makes in the {doc}", f"an event noted by the {role}"]
    return [{"name": n, "text": rng.choice(tpl)} for n in names]


def pick_style(card: dict, rec: dict, need_para: bool) -> dict:
    sts = card["styles"]
    if need_para:
        sts = [s for s in sts if s["container"] not in ST.NO_PARA] or sts
    return fpool.pick(sts, "F6", card["card_id"], rec["uid"], rec.get("ridx", 0))


def pick_wording(card: dict, rec: dict) -> dict:
    ws = sorted(card["wordings"], key=lambda w: w["id"])
    sl = (rec.get("spec") or {}).get("wslots")
    if sl:                      # repair r1 v3b: planned rotation slot (build._wording_slots)
        return ws[sl[min(rec.get("ridx", 0), len(sl) - 1)] % len(ws)]
    return ws[int(unit("wd", card["card_id"], rec["uid"], rec.get("ridx", 0)) * len(ws))]


def c_out_gold(rec: dict, card: dict, names: dict) -> tuple:
    """(gold option text, gold class) from P, the displayed L and the abstain display (rows 33-35, 50)."""
    Pset, L = rec["P"], rec["L"]
    sp = rec["spec"]
    inter = [o for o in L if o in Pset]
    if len(Pset) == 1 and inter:
        return names[inter[0]], "concrete"
    if not inter:
        if sp["none"]:
            return card["none"], "none"
        raise ValueError("None gold not displayed")
    if sp["nei"]:
        return card["nei"], "nei"
    raise ValueError("NEI gold not displayed")


def emit_rules(card: dict, rec: dict, ids: dict) -> tuple[dict, dict]:
    R, case, form = rec["R"], rec["case"], rec["form"]
    P = card["P"]
    attack = rec.get("attack")
    style = pick_style(card, rec, need_para=bool(attack))
    wd = pick_wording(card, rec)
    rng = rng_for("emit", rec["uid"], rec.get("ridx", 0))
    outmap, lform = M_name_map(card, R, form, ids["block"])
    cmpw = {op: rng.choice(ws) for op, ws in RF.CMP_WORDS.items()}
    names = {"out": outmap, "cmp": cmpw}
    ds = P["date_style"]
    frames = card["frames"]
    world = rec.get("world") or P["world"]
    V = RR.card_variant(P, R, form, card["nei"] if form == "c_out" else None,
                        card["none"] if form == "c_out" else None, card["nothing"], frames, world=world)
    V["out_names"] = outmap
    if rec.get("_s5"):
        V["s5"] = True
        V["plans"] = True
    H = M.headings(style)
    dl = card.get("dl_variant")
    policy, num = RF.policy_blocks(R, names, card["defs_style"], "name", H["rules"], dl)
    V["table_num"] = num.get("T")
    reading = RC.reading_lines(P, R, V, form, ds, bool(dl), bool(card.get("attack")))
    blocks = [M.reading_section(H["reading"], reading)] + policy
    options, gold = None, None
    if form == "c_out":
        opt_ids = list(rec["L"])
        options = [outmap[o] for o in opt_ids]
        if rec["spec"]["nei"]:
            options.append(card["nei"])
        if rec["spec"]["none"]:
            options.append(card["none"])
        rng.shuffle(options)
        gold, gcls = c_out_gold(rec, card, outmap)
        if card["defs_style"] in ("one_line", "one_line_examples"):
            ents = gloss_entries(card, [outmap[o] for o in opt_ids], "out", h64(rec["uid"], "g"))
            blocks.append({"type": "section", "heading": H["definitions"],
                           "blocks": [{"type": "defs", "variant": "DV01", "heading": None, "entries": ents}]})
        qtype = "choice"
    elif form == "c_case":
        options = list(rec["cases"])
        rng.shuffle(options)
        gold = rec["gold_case"]
        gcls = "can" if rec["frame"] == "c_case_can" else "cannot"
        qtype = "choice"
    elif form == "c_gap":
        gl = [g for g, _ in rec["gaps"]]
        gt = {tuple(g): RC.gap_text(R, g, case, alt=unit("gapalt", rec["uid"], *map(str, g)) < 0.5) for g in gl}
        options = [gt[tuple(g)] for g in gl] + [card["nothing"]]
        rng.shuffle(options)
        gold = gt[tuple(rec["settle"][0])] if rec["settle"] else card["nothing"]
        gcls = "gap" if rec["settle"] else "nothing"
        qtype = "choice"
    else:
        qtype = "noul"
        gold = rec["gold"]
        gcls = "yes" if gold == 1 else "no"
        if card["defs_style"] in ("one_line", "one_line_examples") and R["event_order"]:
            ents = gloss_entries(card, [R["events"][e]["name"] for e in R["event_order"]], "ev", h64(rec["uid"], "g"))
            blocks.append({"type": "section", "heading": H["definitions"],
                           "blocks": [{"type": "defs", "variant": "DV01", "heading": None, "entries": ents}]})
    blocks += M.example_blocks(card, H)
    card_ir = {"blocks": blocks}
    if rec.get("_s5"):
        doc = rec["_doc_fn"](style)
    elif form == "c_case":
        title = f"{RF.cap(P['case_plural'])} under review"
        doc = RF.record_doc(R, list(rec["cases"]), ds, title)
    else:
        title = f"{RF.cap(P['case_noun'])} file {case}"
        doc = RF.record_doc(R, [case], ds, title)
    if card.get("narrative"):
        doc["blocks"].insert(0, {"type": "para", "text": card["narrative"]})
    if attack:
        doc["blocks"].append({"type": "para", "text": attack})
    inversion = unit("inv", rec["uid"]) < 0.5
    question = RC.question_text(form, rec.get("frame"), R, rec.get("claim"), case, names, inversion)
    fields, res = M.render(style, doc, question, qtype, gold, card_ir, options, wd["text"], ids["id"])
    gaps = rec["gaps"]
    edge = sorted({k for _, k in gaps}) + [f"world:{world}"] + ([lform] if lform != "plain" else [])
    meta = M.make_meta(card_id=card["card_id"], pack=card["pack"]["pid"], sampler=card["sampler"],
                       seed=ids["seed"], structure_hash=rules_hash(R, case, rec), depth=ids["depth"],
                       deep=ids["deep"], format_style=style["id"], wording_id=wd["id"],
                       defs_style=card["defs_style"], twin_of=ids.get("twin_of"), twin_kind=ids.get("twin_kind"),
                       edge=edge, persona_seed=card["pack"].get("persona_seed"), subtype=f"q_{form[1:]}"
                       if form in YN else form, git_sha=ids["git_sha"])
    meta["subtype"] = {"qdet": "q_det", "qest": "q_est", "qplain": "q_plain"}.get(form, form)
    row = M.make_row(rid=ids["id"], group_id=ids["group_id"], call_id=ids["call_id"], fields=fields, qtype=qtype,
                     options=options if qtype == "choice" else None, gold=gold, role=ids.get("role", "train"),
                     meta=meta)
    side = {"id": ids["id"], "kind": "rules", "form": form, "gold_class": gcls,
            "p_set": sorted(outmap[o] for o in rec["P"]), "t_set": sorted(rec["T"]) if rec.get("T") else None,
            "n_gaps": len(gaps), "gap_kinds": [k for _, k in gaps], "gap_positions":
            [G.gap_position(R, case, g) for g, _ in gaps], "frame_id": rec.get("frame") or form,
            "card_variant": world, "label_form": lform, "k": len(options) if options else 2,
            "loader": {"gold_letter": res["gold_letter"], "prompt_sha256": res["prompt_sha256"]},
            "valence": valence_of(card, R, rec), "attack": bool(attack), "struct": export_rules(R, case, rec, outmap),
            "wording_text": wd["text"], "style": style["id"], "frames_card": frames,
            "settle": [list(x) for x in rec.get("settle", [])],
            "cases": rec.get("cases"), "decidable": rec.get("decidable"),
            "switches_stated": switch_keys(reading), "decisive_gap": decisive_of(R, case, rec)}
    return row, side


def switch_keys(lines: list) -> list:
    from .parse_f6 import match_switch
    out = []
    for ln in lines:
        h = match_switch(ln)
        out.append(h[0] if h else "?")
    return sorted(set(out))


def decisive_of(R, case, rec):
    if not case or rec["form"] in ("c_case",):
        return None
    try:
        P = rec.get("T") if rec.get("claim") else rec["P"]
        if P is not None and len(P) < 2:
            return None
        gk = [g for g, _ in rec["gaps"]]
        return [list(d) for d in A.decisive_gaps(R, case, rec.get("claim")) if d in gk]
    except A.Drop:
        return None


def M_name_map(card, R, form, block):
    from .s_rules import name_map
    return name_map(card, R, form, block)


def rules_hash(R: dict, case: str, rec: dict) -> str:
    sym = {"world": R["world"], "local": R.get("local"), "tag": R.get("ev_tag"),
           "attrs": {k: [v["kind"], v.get("lo"), v.get("hi"), len(v.get("vals", []))] for k, v in R["attrs"].items()},
           "notices": R["notices"], "rules": R["rules"], "onlyif": R["onlyif"], "sub": R["subclass"],
           "table": ({k: v for k, v in R["table"].items() if k != "rows" and k != "cols"} if R.get("table") else None),
           "default": R["default"], "facts": R["facts"], "form": rec["form"], "claim": rec.get("claim"),
           "frame": rec.get("frame"), "L": rec.get("L")}
    return M.structure_hash(sym)


def export_rules(R: dict, case: str, rec: dict, outmap: dict) -> dict:
    """The generated structure in surface terms (names), for the G3 comparison with the parse."""
    import copy
    return {"R": copy.deepcopy(R), "case": case, "cases": rec.get("cases"), "outmap": outmap,
            "claim": rec.get("claim"), "L": rec.get("L")}


BAD_WORDS = ("suspend", "refus", "reject", "fine", "penalt", "warning", "revok", "deny", "denied", "withdraw", "close",
             "terminat", "cancel", "impound", "fail", "breach", "complaint", "default", "hold", "stand down", "lapse",
             "return", "pause", "ban", "block", "stop", "seize", "audit", "escalat", "probation")
GOOD_WORDS = ("approv", "grant", "renew", "certif", "accept", "release", "list for sale", "upgrade", "rebate",
              "fast-track", "promot", "credit", "praise", "reward", "assign", "open", "pass", "smooth")


def outcome_valence(card, name: str):
    v = (card["pack"].get("valence") or {}).get(name)
    if v:
        return v
    n = name.lower()
    if any(w in n for w in BAD_WORDS):
        return "bad"
    if any(w in n for w in GOOD_WORDS):
        return "good"
    return None


def valence_of(card, R, rec):
    """Valence of S (s6 'Yes = bad outcome'): the claimed outcome's tag, flipped by 'not'; None = no polarity."""
    cl = rec.get("claim")
    if not cl:
        return None
    v = outcome_valence(card, R["outcomes"][cl["o"]])
    if v is None:
        return None
    if cl.get("neg"):
        v = "good" if v == "bad" else "bad"
    return v
