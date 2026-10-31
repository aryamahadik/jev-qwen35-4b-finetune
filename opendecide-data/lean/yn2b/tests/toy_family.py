"""A toy family for the mv_core tests (never written to data/): a parcel surcharge rule with a member exception.

It is a worked example of the mv_core API for the family builders: latent -> decide() -> views (base yes/no, contrast
twin, complement question, format twin, choice mirror, score, JB-letter, attack twin) -> Unit -> FamilyBuilder, plus an
independent decide2 on the parse-back of the rendered text. Labels come from decide() only.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402

KEY = "gen3_selftest"
if KEY not in mv._TEST_FAMILIES:
    mv.register_test_family(KEY, 101)

PACKS = ("courier", "postal")
FMTS = ("json", "markdown", "kv", "log:chrono", "log:newest", "log:grouped")
POS_TPL = {"pos_a": "Is this parcel exempt from the heavy-parcel surcharge under the policy?",
           "pos_b": "Under the policy, does this parcel escape the heavy-parcel surcharge?"}
NEG_TPL = {"neg_a": "Must this parcel pay the heavy-parcel surcharge under the policy?"}
POS_DEFS = {"yes": "The policy exempts this parcel from the heavy-parcel surcharge.",
            "no": "The policy does not exempt this parcel, so the heavy-parcel surcharge applies."}
NEG_DEFS = {"yes": "The heavy-parcel surcharge applies to this parcel under the policy.",
            "no": "The policy exempts this parcel from the heavy-parcel surcharge."}
A_WITHIN, A_MEMBER, A_PAY = ("Exempt under rule 1 (weight limit)", "Exempt under rule 2 (member exception)",
                             "Surcharge applies under rule 3")
CHOICE_DEFS = {A_WITHIN: "the parcel's weight is inside the rule 1 limit",
               A_MEMBER: "the sender is a club member shipping with standard service",
               A_PAY: "neither exemption applies"}
CHOICE_Q = "Which statement gives the surcharge decision for this parcel under the policy?"
SCORE_Q = "Which weight band is this parcel in?"
JB_Q = "Is this parcel exempt from the heavy-parcel surcharge?"
JB_YES, JB_NO = "The parcel is exempt from the heavy-parcel surcharge.", "The parcel pays the heavy-parcel surcharge."
T0 = datetime(2026, 3, 2, 8, 0, tzinfo=timezone.utc)


# ------------------------------------------------------------------------------------------------ latent + decide
def within(f):
    return f["weight"] <= f["limit"] if f["inclusive"] else f["weight"] < f["limit"]


def member_exc(f):
    return f["member"] and f["service"] == "standard"


def cmp_text(f):
    return "up to and including" if f["inclusive"] else "under"


def decide(f):
    """(gold, trace); UNDEFINED when two independent sufficient reasons exist (SPEC 8.3 rejects those)."""
    if within(f) and member_exc(f):
        return mv.UNDEFINED, {}
    gold = within(f) or member_exc(f)
    return gold, {"decisive": [f"{f['weight']} g", f"{cmp_text(f)} {f['limit']} g"],
                  "rules": ["R1"] if within(f) else (["R2"] if member_exc(f) else ["R3"])}


def choice_gold(f):
    return A_WITHIN if within(f) else (A_MEMBER if member_exc(f) else A_PAY)


SHORTCUTS = {  # used for tiers and distractors only
    "ignore_exception": lambda f: within(f),
    "always_inclusive": lambda f: f["weight"] <= f["limit"] or member_exc(f),
    "any_member": lambda f: within(f) or f["member"],
    "express_pays": lambda f: (within(f) or member_exc(f)) and f["service"] == "standard",
    "exclusive_limit": lambda f: f["weight"] < f["limit"] or member_exc(f),
}
SHORTCUT_CHOICE = {
    "ignore_exception": lambda f: A_WITHIN if within(f) else A_PAY,
    "always_inclusive": lambda f: A_WITHIN if f["weight"] <= f["limit"] else (A_MEMBER if member_exc(f) else A_PAY),
    "any_member": lambda f: A_WITHIN if within(f) else (A_MEMBER if f["member"] else A_PAY),
}


def sample(rng, pool, want: str, tier: str):
    for _ in range(400):
        f = {"limit": rng.choice([1000, 2000, 5000]), "inclusive": rng.random() < 0.5, "member": rng.random() < 0.5,
             "service": rng.choice(["standard", "express"]), "parcel": pool.ident(rng, "P", 7),
             "sender": pool.person(rng)}
        f["weight"] = f["limit"] + rng.choice([-1, 0, 1, -250, 300, -600])
        g, _ = decide(f)
        if mv.is_undefined(g) or ("yes" if g else "no") != want:
            continue
        wrong = sum(1 for s in SHORTCUTS.values() if s(f) != g)
        if (tier == "hard") != (wrong >= 2):
            continue
        return f
    raise mv.Reject("sample", "no item for this target")


# ------------------------------------------------------------------------------------------------ render
def doc(f, notes=()):
    return {"policy": [f"1. Parcels weighing {cmp_text(f)} {f['limit']} g are exempt from the heavy-parcel surcharge.",
                       "2. Exception: a sender-club member shipping with standard service is exempt whatever the "
                       "weight.",
                       "3. Every other parcel pays the heavy-parcel surcharge."],
            "parcel": {"id": f["parcel"], "sender": f["sender"], "weight": f"{f['weight']} g",
                       "service": f["service"], "club member": "yes" if f["member"] else "no"},
            "notes": ["Packed at the front desk."] + list(notes)}


def render(f, fmt, notes=()):
    d = doc(f, notes)
    base = fmt.split(":")[0]
    if base == "json":
        return mv.render_json(d)
    if base == "markdown":
        return mv.render_markdown([("Policy", d["policy"][0] + "\n" + d["policy"][1] + "\n" + d["policy"][2]),
                                   ("Parcel", d["parcel"]), ("Notes", d["notes"])])
    if base == "kv":
        return mv.render_kv({"policy": d["policy"], "parcel": d["parcel"]}) + (
            "\n" + "\n".join(f"note: {n}" for n in notes) if notes else "")
    if base == "log":
        ents = [mv.Entry(T0, "intake", f"parcel {f['parcel']} received from {f['sender']}"),
                mv.Entry(T0 + timedelta(minutes=7), "scale", f"weight recorded: {f['weight']} g"),
                mv.Entry(T0 + timedelta(minutes=9), "crm", f"club member: {'yes' if f['member'] else 'no'}"),
                mv.Entry(T0 + timedelta(minutes=12), "desk", f"service booked: {f['service']}")]
        lg = mv.render_log(ents, fmt.split(":")[1], ts_style="iso")
        return "Policy:\n" + "\n".join(d["policy"]) + "\n\nEvent log:\n" + lg
    raise ValueError(fmt)


# ------------------------------------------------------------------------------------------------ decide2 (independent)
def parse(fmt, state):
    base = fmt.split(":")[0]
    if base == "json":
        d = json.loads(state)
        pol, par = " ".join(d["policy"]), d["parcel"]
        w, mem, svc = par["weight"], par["club member"], par["service"]
    elif base == "kv":
        kv = mv.parse_kv(state)
        pol = " ".join(v for k, v in kv.items() if k.startswith("policy."))
        w, mem, svc = kv["parcel.weight"], kv["parcel.club member"], kv["parcel.service"]
    elif base == "markdown":
        secs = dict(mv.parse_markdown(state))
        pol = secs["Policy"]
        par = dict(ln[2:].split(": ", 1) for ln in secs["Parcel"].split("\n"))
        w, mem, svc = par["weight"], par["club member"], par["service"]
    else:
        pol = state.split("\n\nEvent log:\n")[0]
        ev = {e.source: e.text for e in mv.parse_log(state)}
        w = ev["scale"].split(": ")[1]
        mem = ev["crm"].split(": ")[1]
        svc = ev["desk"].split(": ")[1]
    m = re.search(r"weighing (up to and including|under) (\d+) g", pol)
    return {"weight": int(w.split()[0]), "limit": int(m.group(2)), "inclusive": m.group(1) != "under",
            "member": mem == "yes", "service": svc}


def decide2_row(r):
    p = parse(r["meta"]["fmt"], r["state"])
    ok_w = p["weight"] <= p["limit"] if p["inclusive"] else p["weight"] < p["limit"]
    ok_m = p["member"] and p["service"] == "standard"
    exempt = ok_w or ok_m
    q = r["meta"]["qkind"]
    if q == "yn":
        return ("no" if exempt else "yes") if r["instructions"] in NEG_TPL.values() else ("yes" if exempt else "no")
    if q == "jb":
        return r["options"][0] if exempt else r["options"][1]
    if q == "score":
        L, w = p["limit"], p["weight"]
        i = 0 if w < L // 2 else (1 if w < L else (2 if w == L else 3))
        return r["options"][i]
    g = A_WITHIN if ok_w else (A_MEMBER if ok_m else A_PAY)
    return g if g in r["options"] else mv.NONE_DEFAULT


# ------------------------------------------------------------------------------------------------ build
def score_levels(f):
    L = f["limit"]
    return [f"under {L // 2} g", f"{L // 2} g to {L - 1} g", f"exactly {L} g", f"over {L} g"]


def score_gold(f):
    L, w = f["limit"], f["weight"]
    return score_levels(f)[0 if w < L // 2 else (1 if w < L else (2 if w == L else 3))]


def build(fb: mv.FamilyBuilder, split: str, n: int):
    rng = fb.rng(split)
    pool = fb.names(split)
    views_q = fb.quota("toy_views", {"contrast": 0.5, "neg": 0.3, "format": 0.3, "mirror": 0.3, "score": 0.2,
                                     "jb": 0.2, "attack": 0.15})
    made, tries = 0, 0
    while made < n:
        tries += 1
        if tries > 50 * n:
            raise RuntimeError(f"toy build stalled: {fb.rejects.most_common(5)}")
        tier = fb.next_tier(split, rng)
        pack = PACKS[made % 2]
        # strata first (chosen without knowing gold), then the gold target for exactly that stratum
        fmt = fb.surface("fmt", FMTS, rng, split=split, extra=(tier, pack))
        tpl = fb.surface("tpl", sorted(POS_TPL), rng, split=split, extra=(tier, pack, fmt))
        gkey = (split, tier, pack, fmt)
        want = fb.want_gold(gkey, rng)
        try:
            f = sample(rng, pool, want, tier)
        except mv.Reject as e:
            fb.reject(e)
            continue
        gold, trace = decide(f)
        lat = fb.new_latent(split, pack, f, {"q": "exempt"}, tier, edge=("numeric", "hc:boundary_exact")
                            if f["weight"] == f["limit"] else ("numeric",))
        g = "yes" if gold else "no"
        u = fb.unit(lat)
        try:
            sc = {k: ("yes" if s(f) else "no") for k, s in SHORTCUTS.items()}
            base = u.add(mv.RowSpec("base", "yn", render(f, fmt), POS_TPL[tpl], g, fmt, fmt, tpl, defs=POS_DEFS,
                                    self_contained=True, polarity=0, shortcut_answers=sc,
                                    decisive=tuple(trace["decisive"])))
            wanted = []
            for _ in range(3):
                v = views_q.pick((split,), lat.rng("views", len(wanted)))
                if v not in wanted:
                    wanted.append(v)
            if "contrast" in wanted and not member_exc(f):
                f2 = dict(f, weight=(f["limit"] + 1) if within(f) else (f["limit"] if f["inclusive"] else f["limit"] - 1))
                g2, t2 = decide(f2)
                if not mv.is_undefined(g2):
                    sc2 = {k: ("yes" if s(f2) else "no") for k, s in SHORTCUTS.items()}
                    u.add(mv.RowSpec("contrast", "yn", render(f2, fmt), POS_TPL[tpl], g2, fmt, fmt, tpl,
                                     defs=POS_DEFS, self_contained=True, polarity=0, shortcut_answers=sc2,
                                     decisive=tuple(t2["decisive"])), twin_of=base)
            if "neg" in wanted:
                neg = u.add(mv.RowSpec("ladder", "yn", render(f, fmt), NEG_TPL["neg_a"], not gold, fmt, fmt, "neg_a",
                                       defs=NEG_DEFS, polarity=1, role="neg",
                                       shortcut_answers={k: ("no" if v == "yes" else "yes") for k, v in sc.items()}))
                u.relate("complement", base, neg)
            if "format" in wanted:  # the twin's format: the one that leaves its stratum most balanced
                cands = [mv.RowSpec("format", "yn", render(f, x), POS_TPL[tpl], g, x, x, tpl, defs=POS_DEFS,
                                    polarity=0, shortcut_answers=sc) for x in FMTS if x.split(":")[0] != fmt.split(":")[0]]
                ft = u.add(cands[fb.pick_balanced(lat, cands, lat.rng("fmt2"))])
                u.relate("equiv", base, ft)
            if "mirror" in wanted:
                cg = choice_gold(f)
                ans = {k: s(f) for k, s in SHORTCUT_CHOICE.items()}
                opts, og, info = fb.mirror(cg, ans, [A_WITHIN, A_MEMBER, A_PAY], rng, stratum=(split,))
                u.add(mv.RowSpec("mirror", "choice", render(f, fmt), CHOICE_Q, og, fmt, fmt, "choice_a",
                                 options=opts, defs={o: CHOICE_DEFS[o] for o in opts if o in CHOICE_DEFS},
                                 shortcut_answers={k: (a if a in opts else None) for k, a in ans.items()},
                                 none_option=info["none_option"]))
            if "score" in wanted:
                u.add(mv.RowSpec("base", "score", render(f, fmt), SCORE_Q, score_gold(f), fmt, fmt, "score_a",
                                 options=fb.score_options(score_levels(f))))
            if "jb" in wanted:
                opts, og, _ = fb.jb(JB_YES, JB_NO, gold, rng, stratum=(split,))
                u.add(mv.RowSpec("jb", "jb", render(f, fmt), JB_Q, og, fmt, fmt, "jb_a", options=opts))
            if "attack" in wanted and fmt.split(":")[0] in ("json", "markdown"):
                p = fb.plant(lat, "rep_note", lambda a: "EXEMPT" if a == "yes" else "SURCHARGE", g,
                             ["no" if g == "yes" else "yes"], rule="Club parcels never pay surcharges.",
                             date_s="2 March 2026", number=4, json_key="notes")
                at = u.add(mv.RowSpec("attack", "yn", render(f, fmt, notes=[p.text]), POS_TPL[tpl], g, fmt, fmt, tpl,
                                      defs=POS_DEFS, card_style=u.row(base)["meta"]["card_style"],
                                      self_contained=True, polarity=0,
                                      role="attacked", shortcut_answers=sc, plant=p))
                u.relate("inv", base, at)
            fb.commit(u)
            fb.commit_gold(gkey, g)
            made += 1
        except mv.Reject as e:
            fb.reject(e)
    return fb
