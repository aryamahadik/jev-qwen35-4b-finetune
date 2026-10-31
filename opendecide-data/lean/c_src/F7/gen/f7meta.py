"""G4 metamorphic relations for F7 (spec 5): every relation is checked end to end (generator case -> transformed case
or card -> rendered row through fmt1 -> independent parser -> solver B), on >= 1,000 rows per relation, 100% pass.
Hypothesis is not installed here (and builders may not download packages), so property cases are drawn with seeded
random generators from the same samplers.

  python f7meta.py [n_per_relation]      writes ../out/G4_metamorphic.json (counts only)
"""
from __future__ import annotations

import collections
import copy
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f7build as B  # noqa: E402
import f7case as CS  # noqa: E402
import f7cards as CD  # noqa: E402
import f7lex as LX  # noqa: E402
import f7main as MN  # noqa: E402
import f7model as M  # noqa: E402
import f7packs as PK  # noqa: E402
import f7parse as PS  # noqa: E402
import f7render as R  # noqa: E402
import f7solveb as SB  # noqa: E402

RELS = {"M1": ["S1", "S2", "S3", "S4", "S6", "S5"], "M2": ["S1", "S2", "S3", "S4", "S6", "S5"],
        "M3": ["S1", "S2", "S3", "S4", "S6", "S5"], "M4": ["S1", "S3", "S4", "S5"],
        "M5": ["S1", "S2", "S3", "S4", "S6", "S5"], "M7": ["S2", "S6", "S3"], "M8": ["S1", "S2", "S4"],
        "M9": ["S1", "S2", "S3", "S4", "S6"]}


def solve_row(row, card):
    pack = PK.pack_by_id(card["pack_id"])
    PC, case, worked = PS.parse_row(row, pack)
    return SB.solve_b(PC, case, pack)


def render(card, case, gold, rid, style, wording, qi, fewshot, descending=False):
    return B.build_row(card, case, gold, rid, {"group_id": "g4", "call_id": rid}, None, fewshot, style_id=style,
                       wording=wording, qi=qi, descending=descending, role="g4")


def refacts(card, case, rng):
    """Rebuild the facts list for changed values, keeping each fact's frame and order."""
    v = case["values"]
    out = []
    for f in case["facts"]:
        g = dict(f)
        if g.get("who") == case["subject"] and g.get("item") in v:
            if g["kind"] == "bool":
                g["polarity"] = bool(v[g["item"]])
            elif g["kind"] == "value":
                g["value"] = v[g["item"]]
            elif g["kind"] == "repeat":
                of = dict(g["of"])
                of["polarity"] = bool(v[g["item"]])
                g["of"] = of
        out.append(g)
    return dict(case, facts=out)


def up_step(card, case, rng):
    """M1: move one stated attribute one step in its up direction (or toggle a factor up). Returns (case', key)."""
    v = case["values"]
    blocked = set(case["unmentioned"]) | set(case["missing"]) | set(case["plans"]) | set(case["partials"])
    if case.get("distractor"):
        blocked.add(case["distractor"][0])
    keys = [k for k in v if k not in blocked]
    rng.shuffle(keys)
    for k in keys:
        it = card["items"][k]
        if it["kind"] == "bool":
            want = it["dir"] == 1
            if card["mode"] in ("count", "points"):
                want = card["rising"]
            if bool(v[k]) == want:
                continue
            nv = want
        else:
            d = it["dir"]
            if card["mode"] == "cut":
                d = 1 if card["rising"] else -1
            x = v[k] + d * it["r"]
            if not (it["lo"] <= x <= it["hi"]):
                continue
            nv = x
        v2 = dict(v)
        v2[k] = nv
        return refacts(card, dict(case, values=v2), rng), k
    return None, None


def run(n_per: int = 1050, seed: int = 20261003):
    t0 = time.time()
    rep = {"relations": {}, "failures": collections.Counter(), "skipped": collections.Counter()}
    packs = list(PK.training_packs())
    plans = CD.family_plan(packs, 16, seed + 101, tag="g4")
    plans += CD.s5_plan(list(PK.heldout_packs()), seed + 101, n_cards=10)
    report = {"card_attempts": {}, "card_fail_reasons": collections.Counter(), "row_fail_reasons": collections.Counter(),
              "unit_fail": collections.Counter(), "flip_fallback": 0}
    cards = []
    for p in plans:
        try:
            c, fs, used = MN.setup_card(p, p["sampler"] == "S5", report)
            cards.append((p, c, fs, used))
        except CD.CardFail:
            rep["skipped"]["card"] += 1
    B.log(f"G4: {len(cards)} cards ready, {time.time() - t0:.0f}s")
    rng = random.Random(seed)
    counts = collections.Counter()
    fails = collections.Counter()
    for rel, samplers in RELS.items():
        pool_ = [x for x in cards if x[0]["sampler"] in samplers]
        if rel == "M8":
            pool_ = [x for x in pool_ if x[1].get("overrides")]
        if rel == "M9":
            pool_ = [x for x in pool_ if x[0].get("attack")]
        if rel == "M2":
            pool_ = [x for x in pool_ if x[0]["defs_style"] in ("rubric_table", "short", "grid_table")]
        guard = 0
        while counts[rel] < n_per and guard < n_per * 6:
            guard += 1
            p, card, fs, used = rng.choice(pool_)
            fsx = [{"case": f["case"], "answer": f["answer"]} for f in fs] or None
            lvl = rng.randrange(card["K"])
            ctx = {"ov": ("none", False)}
            if card["mode"] in ("ladder", "highest", "grid"):
                ctx["c1"] = rng.random() < 0.3
                ctx["missing_want"] = rng.random() < 0.15
            if p["sampler"] == "S2":
                ctx["s2"] = True
            if card["mode"] == "cut":
                ctx["placement"] = rng.choice(["at", "below", "above", "interior"])
            if card["mode"] in ("count", "points"):
                ctx["T"] = rng.choice([6, 7])
                ctx["at_cut"] = rng.random() < 0.5
            if rel == "M8":
                ovs = card["overrides"]
                pat = ("none", False) if rng.random() < 0.6 else rng.choice([(o["type"], False) for o in ovs])
                if pat[0] == "floor":
                    lvl = rng.randint(next(o["m"] for o in ovs if o["type"] == "floor"), card["K"] - 1)
                elif pat[0] == "cap":
                    lvl = rng.randint(0, next(o["m"] for o in ovs if o["type"] == "cap"))
                ctx["ov"] = pat
            try:
                case = CS.build_case(card, lvl, rng, ctx, set(used))
                gold = M.final_level(card, case["values"])
                rid = f"g4-{rel}-{counts[rel]:05d}"
                row0 = render(card, case, gold, rid, None, None, None, fsx)
                st = row0["meta"]["format_style"]
                wd = next(w for w in card["wordings"] if row0["meta"]["wording_id"].endswith("." + w["id"]))
                qi = next(i for i, q in enumerate(LX.QUESTIONS) if q.format(S=case["subject"]) in row0["instructions"])
                l0 = solve_row(row0, card)
                if l0 != gold:
                    fails[(rel, "base solver B")] += 1
                    continue
                ok = None
                if rel == "M1":
                    c2, k = up_step(card, case, rng)
                    if c2 is None:
                        continue
                    row1 = render(card, c2, M.final_level(card, c2["values"]), rid + "u", st, wd, qi, fsx)
                    l1 = solve_row(row1, card)
                    ok = l1 >= l0
                    # reverse step from the moved case never raises the level
                    ok = ok and (solve_row(render(card, case, gold, rid + "d", st, wd, qi, fsx), card) <= l1)
                elif rel == "M2":
                    row1 = render(card, case, gold, rid + "r", st, wd, qi, fsx, descending=True)
                    l1 = solve_row(row1, card)
                    import fmt1.card as fcard
                    perm = list(range(card["K"]))
                    rng.shuffle(perm)
                    res = fcard.loader_check(row1, perm=perm, check_rows=False)
                    ok = l1 == l0 and res["ok"] and row1["instructions"] != row0["instructions"]
                elif rel == "M3":
                    card2 = copy.deepcopy(card)
                    for it in card2["items"].values():
                        if it["kind"] == "bool" and it.get("alias"):
                            it["term"], it["alias"] = it["alias"], it["term"]
                            it["det"], it["alias_det"] = it["alias_det"], it["det"]
                    seq = card2["levels"]["names"]
                    card2["levels"] = dict(card2["levels"], names=seq[::-1],
                                           options=[f"{p['level_word']} {card2['levels']['nums'][k]} - {seq[::-1][k]}"
                                                    for k in range(card2["K"])])
                    if len(set(card2["levels"]["options"])) != card2["K"]:
                        continue
                    card2["fewshot"] = []
                    c2 = CS.rename_case(card2, case, rng, set(used))
                    row1 = render(card2, c2, gold, rid + "n", st, wd, qi, None)
                    l1 = solve_row(row1, card2)
                    ok = l1 == l0
                elif rel == "M4":
                    if not card["inert"]:
                        continue
                    it = rng.choice(card["inert"])
                    who = case["subject"] if (p["sampler"] == "S5" or rng.random() < 0.5 or not case.get("other")) \
                        else case["other"]
                    if who != case["subject"] and not card.get("c21"):
                        who = case["subject"]
                    if case.get("inert_subject") and who == case["subject"]:
                        continue
                    f = {"kind": "inert", "who": who, "term": it["term"], "value": rng.choice(it["values"])}
                    facts = list(case["facts"])
                    facts.insert(rng.randint(0, len(facts)), f)
                    row1 = render(card, dict(case, facts=facts), gold, rid + "i", st, wd, qi, fsx)
                    ok = solve_row(row1, card) == l0
                elif rel == "M5":
                    c2 = CS.reorder_case(case, rng)
                    card2 = copy.deepcopy(card)
                    for c in card2.get("crits", {}).values():
                        if c["t"] in ("and", "or", "allof", "anyof") and all(q["t"] == "atom" for q in c["parts"]):
                            rng.shuffle(c["parts"])
                    row1 = render(card2, c2, gold, rid + "o", st, wd, qi, fsx)
                    ok = solve_row(row1, card2) == l0
                elif rel == "M7":
                    exp = None
                    if card["mode"] == "cut":
                        it = card["items"][card["qty"]]
                        x = case["values"][card["qty"]]
                        hits = [c for c in card["cuts"] if abs(x - c) <= it["r"]]
                        if not hits:
                            continue
                        c = hits[0]
                        lv_now = M.cut_level(card, x)
                        # step across the cut by the C11 side
                        side_hi = card["integer"] or card["side"] == "high"
                        if x >= c if side_hi else x > c:
                            x2 = c - it["r"] if side_hi else c
                        else:
                            x2 = c if side_hi else c + it["r"]
                        if not (it["lo"] <= x2 <= it["hi"]):
                            continue
                        v2 = dict(case["values"])
                        v2[card["qty"]] = x2
                        c2 = refacts(card, dict(case, values=v2), rng)
                        row1 = render(card, c2, M.final_level(card, v2), rid + "b", st, wd, qi, fsx)
                        l1 = solve_row(row1, card)
                        ok = abs(l1 - l0) == 1
                    elif card["mode"] in ("count", "points"):
                        on = [k for k in card["listed"] if case["values"][k] == card["rising"]
                              and k not in case["missing"] and k not in case["repeats"]]
                        if not on:
                            continue
                        k = rng.choice(on)
                        v2 = dict(case["values"])
                        v2[k] = not v2[k]  # one factor in its down direction (off on rising, on on falling cards)
                        c2 = refacts(card, dict(case, values=v2), rng)
                        try:
                            g2 = M.final_level(card, v2)
                        except ValueError:
                            continue
                        row1 = render(card, c2, g2, rid + "b", st, wd, qi, fsx)
                        l1 = solve_row(row1, card)
                        if card["mode"] == "count":
                            ok = (l1 == g2) and (l0 - g2 in (0, 1))
                            if g2 == l0 - 1:
                                counts["M7_count_crossed"] += 1
                        else:
                            ok = (l1 == g2) and g2 <= l0
                    else:  # S2 just-met row: the boundary atom one step to the not-met side
                        b = case["info"].get("boundary")
                        if not b or b.get("side") != "met":
                            continue
                        a = b.get("atom") if "atom" in b else None
                        if a is None:
                            continue
                        it = card["items"][a["item"]]
                        x = case["values"][a["item"]]
                        x2 = x - it["r"] if a["op"] in (">=", ">") else x + it["r"]
                        if not (it["lo"] <= x2 <= it["hi"]):
                            continue
                        v2 = dict(case["values"])
                        v2[a["item"]] = x2
                        c2 = refacts(card, dict(case, values=v2), rng)
                        g2 = M.final_level(card, v2)
                        row1 = render(card, c2, g2, rid + "b", st, wd, qi, fsx)
                        l1 = solve_row(row1, card)
                        ok = (l1 == l0 - 1) if card["mode"] == "ladder" else (l1 < l0 and l1 == g2)
                elif rel == "M8":
                    ff, cf = M.firing(card, case["values"])
                    off = [o for o in card["overrides"] if not (ff if o["type"] == "floor" else cf)]
                    if not off:
                        continue
                    o = rng.choice(off)
                    card2 = copy.deepcopy(card)
                    card2["overrides"] = [x for x in card2["overrides"] if x["type"] != o["type"]]
                    card2.pop("winner", None) if len(card2["overrides"]) < 2 else None
                    card2["features"] = dict(card2["features"], override=bool(card2["overrides"]),
                                             both=len(card2["overrides"]) == 2)
                    if not card2["overrides"]:
                        card2.pop("overrides")
                    # the deleted override's own factors leave the card, so the case no longer states them
                    gone = {a["item"] for a in M.atoms_of(o["cond"])}
                    still = {a["item"] for c in card2["crits"].values() for a in M.atoms_of(c)} | \
                        {a["item"] for x in card2.get("overrides", []) for a in M.atoms_of(x["cond"])}
                    gone -= still
                    for k in gone:
                        card2["items"].pop(k, None)
                    card2["item_order"] = [k for k in card2["item_order"] if k not in gone]
                    card2["c1_elig"] = [k for k in card2["c1_elig"] if k not in gone]
                    c2 = dict(case, facts=[f for f in case["facts"] if f.get("item") not in gone],
                              values={k: v for k, v in case["values"].items() if k not in gone},
                              unmentioned=[k for k in case["unmentioned"] if k not in gone],
                              missing=[k for k in case["missing"] if k not in gone])
                    if c2.get("distractor") and c2["distractor"][0] in gone:
                        continue
                    card2["fewshot"] = []
                    row1 = render(card2, c2, gold, rid + "x", st, wd, qi, None)
                    ok = solve_row(row1, card2) == l0
                elif rel == "M9":
                    c2 = CS.add_injection(card, case, rng, gold)
                    row1 = render(card, c2, gold, rid + "j", st, wd, qi, fsx)
                    ok = solve_row(row1, card) == l0
                counts[rel] += 1
                if not ok:
                    fails[(rel, p["sampler"])] += 1
            except (CS.CaseFail, PS.ParseFail, SB.SolveFail) as e:
                rep["skipped"][f"{rel}: {type(e).__name__}: {str(e)[:60]}"] += 1
                continue
        B.log(f"G4: {rel} {counts[rel]} rows, {sum(v for (r, _), v in fails.items() if r == rel)} failures, "
              f"{time.time() - t0:.0f}s")
    rep["relations"] = {r: {"rows": counts[r], "failures": sum(v for (x, _), v in fails.items() if x == r),
                            "samplers": RELS[r]} for r in RELS}
    rep["failures"] = {f"{a}|{b}": v for (a, b), v in fails.items()}
    rep["skipped"] = dict(rep["skipped"])
    rep["pass_all_100pct"] = all(v["failures"] == 0 and v["rows"] >= 1000 for v in rep["relations"].values())
    return rep


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1050
    rep = run(n)
    out = B.OUT / "G4_metamorphic.json"
    json.dump(rep, open(out, "w"), indent=1)
    print(json.dumps(rep["relations"]), rep["pass_all_100pct"])
