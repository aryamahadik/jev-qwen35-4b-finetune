"""F7 generator driver: cards -> rows -> G3 (parse + solver B + structure hash + option_level) -> outputs.

  python f7build.py candidates      round-1 candidate pool (1.5 x 3,150 rows, training samplers S1-S4, S6)
  python f7build.py qc              separate G6 QC sample (>= 5,000 rows, fresh cards, same samplers)
  python f7build.py mixdev          400 mix-tuning dev items from S5 (held-out packs and styles)
  python f7build.py smoke N         N cards per sampler, few rows (development)
Progress lines go to c_build/progress_phase2.log prefixed [F7]; scratch and logs stay in c_src/F7/tmp/.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
import random
import sys
import time
import traceback
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f7render as R  # noqa: E402  (sets the fmt1 path)
from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool  # noqa: E402
from fmt1.render import FormatError  # noqa: E402

import f7case as CS  # noqa: E402
import f7cards as CD  # noqa: E402
import f7lex as LX  # noqa: E402
import f7model as M  # noqa: E402
import f7packs as PK  # noqa: E402
import f7parse as PS  # noqa: E402
import f7rows as RW  # noqa: E402
import f7solveb as SB  # noqa: E402

LEAN = HERE.parents[2]
OUT = HERE.parent / "out"
TMP = HERE.parent / "tmp"
PROGRESS = LEAN / "c_build/progress_phase2.log"
SEED = 20261003
GIT_SHA = "18c024c413e354209fddd98a26b95d37b4b908b4"
F2W = LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"
FT_OK = ["FT01", "FT02", "FT03", "FT05", "FT06", "FT07", "FT08", "FT09", "FT11", "FT12", "FT13", "FT14", "FT15",
         "FT16", "FT04"]


def log(msg: str) -> None:
    line = f"[F7] {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def wordings_by_family() -> dict:
    out = collections.defaultdict(list)
    for l in open(F2W, encoding="utf-8"):
        w = json.loads(l)
        if w.get("family") == "F7":
            out[w["wording_family"]].append(w)
    return out


WORDINGS = wordings_by_family()


# ------------------------------------------------------------------------------------------------ card finalize
def finalize(card: dict, plan: dict, pack: dict, held_out: bool) -> dict:
    rng = CD.rng_for("finalize", plan["card_id"])
    card["levels"] = CD.level_presentation(plan, rng)
    card["date_fmt"] = rng.choice(LX.DATE_FORMATS)
    dates = [it for it in card["items"].values() if it["kind"] == "date"]
    start = M.day(dt.date.fromisoformat(pack["date_start"]))
    card["R"] = max([it["hi"] for it in dates], default=start + min(pack["date_span"], 500))
    for it in dates:
        it["hi"] = card["R"]
    cont = plan["container"]
    card["container"] = cont
    has_bool = any(it["kind"] == "bool" for it in card["items"].values())
    s = plan["sampler"]
    card["layout"] = "narrative" if (s == "S4" or (s in ("S6", "S5") and cont in ("prose", "memo", "email_thread",
                                                                                  "bullet_sop"))) else "fields"
    card["c15"] = None
    if cont in CD.STRUCTURED and has_bool and s in ("S1", "S2", "S3", "S4"):
        card["c15"] = "key" if cont in ("json", "yaml") else "blank"
    card["c21"] = s in ("S1", "S3", "S4") and (bool(pack["inert"]) or s == "S4")
    card["markers"] = ("yes", "no")  # one marker pair everywhere, so negcount's k_all over state tracks the cue count
    card["remark_key"] = rng.choice(["remark", "comment"])
    card["ids"] = pack["ids"]
    card["singular"] = pack["singular"]
    card["ents"] = pack["plural"]
    card["inert"] = pack["inert"]
    card["roles"] = (pack["roles"] + ["review desk", "intake desk"])[:2]
    if card["roles"][0] == card["roles"][1]:
        card["roles"] = ["intake desk", "review desk"]
    card["low_word"] = rng.choice(["range", "or fewer"])
    card["item_order"] = RW.item_order(card)
    for o in card.get("overrides", []):
        for a in M.atoms_of(o["cond"]):
            if a["item"] not in card["item_order"]:
                card["item_order"].append(a["item"])
    card["features"] = RW.card_features(card, plan)
    card["c1_elig"] = RW.c1_eligible(card)
    bools = [it for it in card["items"].values() if it["kind"] == "bool"]
    card["c1_form"] = "generic" if not bools or rng.random() < 0.5 else ("one" if len(bools) <= 2 else "list")
    card["aliases_on"] = bool(bools) and rng.random() < 0.3 and all(it.get("alias") for it in bools)
    if card["mode"] in ("count", "points"):
        m = len(card["listed"])
        lst = set(card["listed"])
        pool_f = [f for f in pack["fillers"]]
        f_hi = min(m + 4, 16 - m, len(pool_f))
        # r1d: absence-cue totals T in {T0, T0 + 1}, T0 = max(6, m) (within m..f, Z02), cycled per level on every card
        # (level-independent, 6.3); f >= T0 + 1 so every row can reach both
        t0 = max(6, m)
        card["cue_T"] = (t0, t0 + 1)
        if f_hi < t0 + 1:
            raise CD.CardFail("fillers")
        card["n_fillers"] = rng.randint(t0 + 1, f_hi)
        card["filler_pool"] = pool_f
    card["dv"] = rng.choice(["DV01", "DV02", "DV03", "DV04", "DV05", "DV06"]) if plan["defs_style"] in (
        "one_line", "one_line_examples") else rng.choice(["DV21", "DV22", "DV23", "DV24"])
    card["ft"] = rng.choice(FT_OK)
    card["table_cols"] = rng.choice(LX.TABLE_COLS)
    card["task_line"] = rng.choice(LX.TASK_LINES)
    wf = WORDINGS[plan["wording_family"]]
    card["wordings"] = rng.sample(wf, min(len(wf), rng.choice([5, 6])))
    cands = pool.styles(held_out=held_out, container=cont, exclude_flags=("adds_numbers",))
    if not cands:
        cands = pool.styles(held_out=held_out, container=cont)
    if card.get("c21"):
        # G12 r1d: the C21 line names the row's subject, so it is the one row-specific line of the card text. Card
        # styles that join card blocks without blank lines (blank_between False) fuse it with the rubric, C-lines and
        # worked cases into one paragraph, and that whole card text then differs per row (row-level text: MinHash
        # near-duplicates between rows of one card). C21 cards use styles that keep card blocks as paragraphs.
        # (r1d: the blockquote wrapper turns blank lines into ">" lines, so it fuses the paragraphs too)
        sep = [x for x in cands if pool.card_style(x["card_style"])["blank_between"]
               and pool.card_style(x["card_style"])["wrapper"] != "quote"]
        cands = sep or cands
    ranked = pool.card_style_set(cands, len(cands), "F7", plan["card_id"])
    picked, skins = [], set()
    for x in ranked:  # distinct skins first, so a card's rows spread over render templates (G11)
        if x["skin"] not in skins:
            picked.append(x)
            skins.add(x["skin"])
        if len(picked) == 5:
            break
    if len(picked) < 2:
        for x in ranked:
            if len(picked) >= 3:
                break
            if x not in picked:
                picked.append(x)
    card["style_set"] = [x["id"] for x in picked]
    if plan["sampler"] in ("S1", "S2", "S4"):
        # G12 r1c: one format style per S1 / S2 / S4 card. Styles lay the moved card text (rubric, C-lines, worked
        # cases) out differently, so with several styles on a card no layout of that text reaches half the card's
        # rows and it reads as row-level text: rows of one card then share most of their row-level 5-grams (MinHash
        # near-duplicates). Styles still vary across cards (ranked per card as before); render templates per sampler x
        # container x state skeleton stay far under 2% (G11).
        card["style_set"] = card["style_set"][:1]
    card["style_all"] = sorted(x["id"] for x in cands)
    # depth (2.7): c + o + a
    cmax = 0
    for c in card.get("crits", {}).values():
        cmax = max(cmax, M.n_ops(c))
    for o in card.get("overrides", []):
        cmax = max(cmax, M.n_ops(o["cond"]))
    a = max(0, card.get("P", 0) - 1) if card["mode"] == "points" else 0
    card["depth"] = cmax + len(card.get("overrides", [])) + a
    card["deep"] = cmax > 2 or len(card.get("overrides", [])) > 1 or (card["mode"] == "points" and card.get("P", 4) > 4)
    return card


# ------------------------------------------------------------------------------------------------ one row
def row_fields(card: dict, case: dict, row_id: str, rng_key: str, *, descending: bool = False,
               fewshot: list | None = None, style_id: str | None = None, wording: dict | None = None,
               qi: int | None = None) -> tuple[dict, dict, str, dict, str]:
    S = case["subject"]
    q = LX.QUESTIONS[qi if qi is not None else int(pool.unit_hash("q", card["card_id"], rng_key) * len(LX.QUESTIONS))]
    question = q.format(S=S)
    w = wording or pool.pick([{"id": x["id"], **x} for x in card["wordings"]], "F7w", card["card_id"], rng_key)
    cir = R.card_ir(card, S, descending=descending, fewshot=fewshot)
    order = [style_id] if style_id else sorted(card["style_set"], key=lambda sid: pool.unit_hash(card["card_id"], rng_key, sid))
    order += [x for x in sorted(card["style_all"], key=lambda sid: pool.unit_hash(card["card_id"], rng_key, sid))
              if x not in order]
    last = None
    for sid in order:
        st = pool.style(sid)
        try:
            f = R.render_fields(st, card, case, cir, question, w["text"])
            return f, st, question, w, sid
        except FormatError as e:
            last = e
            continue
    raise CS.CaseFail(f"no style renders: {last}")


def build_row(card: dict, case: dict, gold: int, row_id: str, ids: dict, twin: dict | None, fewshot, *,
              descending=False, style_id=None, wording=None, qi=None, role="train") -> dict:
    f, st, question, w, sid = row_fields(card, case, row_id, row_id, descending=descending, fewshot=fewshot,
                                         style_id=style_id, wording=wording, qi=qi)
    opts = card["levels"]["options"]
    plan = card["plan"]
    edge = RW.conv_elements(card, case, gold, {})
    b = case.get("info", {}).get("boundary")
    if b is not None:
        edge.append({"kind": "boundary", "placement": b["placement"], "cmp": b["cmp"]})
    meta = {"family": "F7", "spec_id": LX.SPEC_ID, "spec_sha256": LX.SPEC_SHA256, "card_id": card["card_id"],
            "domain_pack": card["pack_id"], "sampler": card["sampler"], "gen_version": LX.GEN_VERSION,
            "git_sha": GIT_SHA, "seed": SEED, "structure_hash": RW.structure_hash(card, case["values"]),
            "difficulty_bin": None, "crowd_pg": None, "depth": card["depth"], "deep": card["deep"],
            "format_style": sid, "wording_id": f"{plan['wording_family']}.{w['id']}",
            "defs_style": "few_shot" if plan.get("fewshot") else plan["defs_style"],
            "base_defs_style": plan["defs_style"], "twin_of": twin["of"] if twin else None,
            "twin_kind": twin["kind"] if twin else None, "text_source": None,
            "licence": "CC0 1.0 (program-generated)", "edge": edge,
            "option_level": {opts[k]: k for k in range(card["K"])},
            "subtype": "cutpoint" if card["mode"] == "cut" else card["mode"],
            "persona_seed": PK.load_persona(card["pack_id"]), "K": card["K"], "mode": card["mode"],
            "label_form": plan["name_form"], "container": st["container"], "defs_variant": card["dv"],
            "fewshot_template": card["ft"] if fewshot else None, "role": role,
            "row_kind": (twin or {}).get("variant") or "base",
            "case_features": {"unmentioned": len(case.get("unmentioned") or []), "missing": len(case.get("missing") or []),
                              "plans": len(case.get("plans") or []), "partials": len(case.get("partials") or []),
                              "repeats": len(case.get("repeats") or []), "fillers": len(case.get("fillers") or []),
                              "inert_subject": bool(case.get("inert_subject")),
                              "other": ("distractor" if case.get("distractor") else "inert" if case.get("other") else None),
                              "injected": case.get("inject") is not None,
                              "cue_target_met": case.get("cue_target_met")}}
    row = {"id": row_id, "group_id": ids["group_id"], "call_id": ids["call_id"], "source": "c_f7_ordinal",
           "state": f["state"], "qtype": "choice", "instructions": f["instructions"], "options": list(opts),
           "gold": opts[gold], "role": role, "card": f["card"], "meta": meta}
    if role == "qc":  # L13: G6 inputs kept apart by content (a) state + wording + question, (c) card content
        ins = f["instructions"]
        moved = ins
        for x in (w["text"], question):
            moved = moved.replace(x, "")
        meta["g6_parts"] = {"wording": w["text"], "question": question, "card_content": (moved.strip() + "\n" +
                                                                                       (f["card"] or "")).strip()}
    must = R.must_show(R.card_ir(card, case["subject"], descending=descending, fewshot=fewshot), question, w["text"])
    res = fcard.loader_check(row, must_show=must, seed=f"F7-G15:{SEED}")
    if not res["ok"]:
        raise CS.CaseFail("loader_check: " + "; ".join(res["problems"][:3]))
    row["_gold_letter"] = res["gold_letter"]
    row["_perm"] = res["perm"]
    return row


def g3_check(row: dict, card: dict, pack: dict, gold: int) -> None:
    """G3: parse the four fields back (independent parser), re-solve with solver B, compare structure hash and
    option_level. Raises on any disagreement."""
    PC, case, worked = PS.parse_row(row, pack)
    if PC["option_level"] != row["meta"]["option_level"]:
        raise SB.SolveFail("option_level differs")
    lb = SB.solve_b(PC, case, pack)
    if lb != gold:
        raise SB.SolveFail(f"solver B {lb} != solver A {gold}")
    h = parsed_structure_hash(PC, case)
    if h != row["meta"]["structure_hash"]:
        raise SB.SolveFail("structure hash differs")
    for wc, ans in worked:
        lw = SB.solve_b(PC, wc, pack)
        if PC["option_level"][ans] != lw:
            raise SB.SolveFail("worked case level differs")
    return PC


def parsed_structure_hash(PC: dict, case: dict) -> str:
    """The parser's own canonical form (item order by first appearance in the printed rubric)."""
    order = []

    def add(t):
        if t not in order:
            order.append(t)

    def walk(c):
        if c["t"] == "atom":
            add(c["a"]["term"])
        elif c["t"] in ("and", "or", "allof", "anyof"):
            for p in c["parts"]:
                walk(p)
        elif c["t"] == "unless":
            walk(c["a"])
            add(c["b"]["term"])
        elif c["t"] == "onlyif":
            walk(c["main"])
            add(c["c"]["term"])
    K = PC["K"]
    mode = PC["mode"]
    if mode in ("count", "points"):
        for t in PC["listed"]:
            add(t)
    elif mode == "cut":
        add(PC["qty_term"])
    elif mode == "grid":
        for k in range(1, K):
            for a in PC["grid"][k]:
                add(a["term"])
    else:
        for k in range(1, K):
            walk(PC["crits"][k])
        ovs = sorted(PC.get("overrides", []), key=lambda o: 0 if o["type"] == "floor" else 1)
        for o in ovs:
            walk(o["cond"])
    idx = {t: i for i, t in enumerate(order)}
    ranks = PC.get("ranks") or []

    def ca(a):
        if a["kind"] == "bool":
            return [idx[a["term"]], a["op"]]
        if a["op"] == "within":
            return [idx[a["term"]], "within", str(a["t"]), str(a["N"])]
        if a["kind"] == "ord":
            return [idx[a["term"]], a["op"], str(ranks.index(a["rank"]))]
        return [idx[a["term"]], a["op"], str(Fraction(a["t"]))]

    def cc(c):
        t = c["t"]
        if t == "atom":
            return ca(c["a"])
        if t in ("and", "or", "allof", "anyof"):
            return [{"allof": "and", "anyof": "or"}.get(t, t), [cc(p) for p in c["parts"]]]
        if t == "unless":
            return ["unless", cc(c["a"]), ca(c["b"])]
        if t == "onlyif":
            return ["onlyif", cc(c["main"]), ca(c["c"])]
    can = {"K": K, "mode": mode}
    if mode in ("ladder", "highest"):
        can["crits"] = [cc(PC["crits"][k]) for k in range(1, K)]
        can["ov"] = sorted([[o["type"], cc(o["cond"]), o["m"]] for o in PC.get("overrides", [])])
        if len(PC.get("overrides", [])) == 2:
            can["winner"] = PC["winner"]
    elif mode in ("count", "points"):
        bands = []
        for k in range(K):
            lo, hi = PC["bands"][k]
            bands.append([0 if lo is None else lo, hi])
        can["bands"] = bands
        if mode == "points":
            can["w"] = [PC["weights"][t] for t in order]
    elif mode == "cut":
        can["ranges"] = parsed_cut_intervals(PC)
    elif mode == "grid":
        can["grid"] = [[ca(a) for a in PC["grid"][k]] for k in range(1, K)]
    vals = []
    for t in order:
        if t in case["values"]:
            v = case["values"][t]
            vals.append(str(Fraction(v)) if not isinstance(v, bool) else str(v))
        else:
            vals.append(str(bool(case["presence"].get(t, False))))
    can["v"] = vals
    return hashlib.sha256(json.dumps(can, sort_keys=True).encode()).hexdigest()[:32]


def parsed_cut_intervals(PC: dict) -> list:
    K = PC["K"]
    rs = [PC["ranges"][k] for k in range(K)]
    integer = all(rg[0] in ("int", "ge", "le") for rg in rs)
    out = []
    if integer:
        def low(rg):
            return -10 ** 12 if rg[0] == "le" else rg[1]
        smallest = min(range(K), key=lambda k: low(rs[k]))
        for k, rg in enumerate(rs):
            if rg[0] == "int":
                lo, hi = rg[1], rg[2]
            elif rg[0] == "ge":
                lo, hi = rg[1], None
            else:
                lo, hi = None, rg[1]
            if k == smallest:
                lo = None
            out.append([None if lo is None else str(Fraction(lo)), None if lo is None else True,
                        None if hi is None else str(Fraction(hi)), None if hi is None else True])
        return out
    for rg in rs:
        if rg[0] == "half":
            _, lo, lo_in, hi, hi_in = rg
        elif rg[0] == "ge":
            lo, lo_in, hi, hi_in = rg[1], True, None, None
        else:
            lo, lo_in, hi, hi_in = None, None, rg[1], True
        out.append([None if lo is None else str(Fraction(lo)), None if lo is None else lo_in,
                    None if hi is None else str(Fraction(hi)), None if hi is None else hi_in])
    return out
